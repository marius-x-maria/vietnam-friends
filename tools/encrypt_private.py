"""Encrypt the private trip content into index.html.

Reads the clear-text fragment (place catalogue, Info tab) from private/site.local.html (git-ignored,
built by private/build_fragment.py) and the site code from .env (FRIENDS_CODE). Writes an AES-256-GCM
payload, key derived by PBKDF2-SHA256, into the PRIVATE block of index.html. The page decrypts it
in the browser with Web Crypto once the code is typed.

Strength = the code's entropy only (16 random chars from a-z0-9 ~ 83 bits). Never use a short code.

Usage:
  python tools/encrypt_private.py [--json]
  FRIENDS_CODE=<throwaway> python tools/encrypt_private.py   (browser tests; the env var wins over .env)
Exit codes: 0 ok, 1 tool failed (missing input, bad config), 2 ran but verification failed.
Dependency: `cryptography` (pip install cryptography) - stdlib has no AES-GCM.
"""
import argparse, base64, html, json, os, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "private" / "site.local.html"
PAGE = ROOT / "index.html"
ENV = ROOT / ".env"
ITERATIONS = 300_000  # keep identical to PRIVATE_ITER in index.html
BLOCK = re.compile(r"(/\*PRIVATE:BEGIN\*/).*?(/\*PRIVATE:END\*/)", re.S)
# Public facts that may appear in the page in clear text (city names, generic words)
PUBLIC_OK = {"hà nội", "phú quốc", "hồ chí minh city", "saigon"}


def normalise(code: str) -> str:
    # Same rule as the page: lowercase, drop spaces and dashes.
    return re.sub(r"[\s\-]", "", code).lower()


def read_code() -> str:
    raw = os.environ.get("FRIENDS_CODE")
    if not raw:
        if not ENV.exists():
            raise SystemExit(f"missing {ENV} - add a line FRIENDS_CODE=<16+ random chars>")
        for line in ENV.read_text(encoding="utf-8").splitlines():
            if line.startswith("FRIENDS_CODE="):
                raw = line.split("=", 1)[1].strip()
                break
        else:
            raise SystemExit(f"FRIENDS_CODE not found in {ENV} - add it")
    code = normalise(raw)
    if len(code) < 16:
        raise SystemExit("FRIENDS_CODE is shorter than 16 chars - generate a longer random code")
    return code


def plain_terms(fragment: str) -> list[str]:
    # Every place name and address in the fragment; none may appear in a publishable file.
    m = re.search(r'<script type="application/json" id="vf-data">(.*?)</script>', fragment, re.S)
    if not m:
        return []
    data = json.loads(m.group(1).replace("<\\/", "</"))
    out = set()
    for it in data["items"]:
        for k in ("n", "a", "note"):
            v = html.unescape(str(it.get(k, ""))).strip()
            if v and v.lower() not in PUBLIC_OK:
                out.add(v)
    return sorted(out)


def publishable_files() -> list[Path]:
    # Every file git would commit: tracked + untracked-but-not-ignored.
    out = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard"],
                         cwd=ROOT, capture_output=True, text=True, encoding="utf-8", check=True).stdout
    return [ROOT / p for p in out.splitlines() if p and (ROOT / p).is_file()]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    def done(ok, summary, findings=(), code=0):
        if args.json:
            print(json.dumps({"ok": ok, "summary": summary, "findings": list(findings), "outputs": [str(PAGE)] if ok else []}))
        else:
            for f in findings:
                print(f"- {f}")
            print(summary)
        return code

    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        from cryptography.hazmat.primitives import hashes
    except ImportError:
        return done(False, "cryptography not installed - run: pip install cryptography", code=1)
    if not SRC.exists():
        return done(False, f"missing {SRC} - run: python private/build_fragment.py", code=1)
    try:
        code = read_code()
    except SystemExit as e:
        return done(False, str(e), code=1)

    fragment = SRC.read_text(encoding="utf-8")
    salt, iv = os.urandom(16), os.urandom(12)
    key = PBKDF2HMAC(hashes.SHA256(), 32, salt, ITERATIONS).derive(code.encode())
    ct = AESGCM(key).encrypt(iv, fragment.encode("utf-8"), None)
    b64 = lambda b: base64.b64encode(b).decode()
    payload = json.dumps({"s": b64(salt), "i": b64(iv), "c": b64(ct)})

    raw = PAGE.read_bytes().decode("utf-8")
    if not BLOCK.search(raw):
        return done(False, "PRIVATE markers not found in index.html - restore the /*PRIVATE:BEGIN*/null/*PRIVATE:END*/ block", code=1)
    PAGE.write_bytes(BLOCK.sub(lambda m: f"{m.group(1)}{payload}{m.group(2)}", raw, count=1).encode("utf-8"))

    # Verify: round-trip decrypt, and no clear-text place name or address in any publishable file.
    findings = []
    p = json.loads(BLOCK.search(PAGE.read_text(encoding="utf-8")).group(0)[len("/*PRIVATE:BEGIN*/"):-len("/*PRIVATE:END*/")])
    back = AESGCM(PBKDF2HMAC(hashes.SHA256(), 32, base64.b64decode(p["s"]), ITERATIONS).derive(code.encode())).decrypt(
        base64.b64decode(p["i"]), base64.b64decode(p["c"]), None).decode()
    if back != fragment:
        findings.append("round-trip decrypt does not match the source fragment")
    terms = plain_terms(fragment)
    if not terms:
        findings.append("no terms extracted from the fragment - the plaintext check proved nothing")
    check = [t.lower() for t in terms]
    for f in publishable_files():
        try:
            text = html.unescape(f.read_text(encoding="utf-8")).lower()
        except (UnicodeDecodeError, OSError):
            continue
        hits = [t for t in check if t in text]
        if hits:
            findings.append(f"{len(hits)} private term(s) in clear text in {f.relative_to(ROOT)} (e.g. {hits[0]!r}) - remove them before committing")
    if findings:
        return done(False, "encrypted, but verification FAILED", findings, code=2)
    return done(True, f"encrypted {len(fragment)} chars into index.html; round-trip ok; 0 of {len(terms)} private terms in clear text")


if __name__ == "__main__":
    sys.exit(main())
