---
name: vietnam-friends-map
description: Generated map of vietnam-friends - code relations, doc links, health
tags: [map, generated]
---

# Map — vietnam-friends

Generated 2026-11-27 by `tools/build_map.py` (deterministic, do not edit). Read this instead of exploring; open files only when needed.

## Code
| File | Purpose | Defines | Imports | Run by |
|---|---|---|---|---|
| `private/build_fragment.py` | Build the private clear-text fragment for the vietnam-friends site. | q, exc, food, js, main |  | — |
| `tools/encrypt_private.py` | Encrypt the private trip content into index.html. | normalise, read_code, plain_terms, publishable_files, main |  | .session-report.md, AGENT.md, private/NEXT.md |

## Documents
| File | What it answers | Links out | In |
|---|---|---|---|
| `AGENT.md` | Agent briefing for the vietnam-friends trip site - role, decisions, capability registry, rules | AGENT, airports-terminals-2026-11-23, eugen-picks-prices-pin | 2 |
| `knowledge-base/airports-terminals-2026-11-23.md` | Which airport and terminal the friends use in Saigon, Phú Quốc and Hà Nội, domestic vs international, with sou | AGENT | 3 |
| `knowledge-base/info-tab-facts-2026-11-23.md` | Sourced facts behind the Info tab (apps, airport fast track, entry, practical tips) for the Vietnam trip, fetc | — | 3 |
| `knowledge-base/README.md` | Map of Content - sourced snapshots for the vietnam-friends site | airports-terminals-2026-11-23, eugen-picks-prices-pins-2026- | 1 |
| `private/NEXT.md` | NEXT: continue here (private, git-ignored) | airports-terminals-2026-11-23, fetch-snapshot-log, travel-re | 0 |
| `README.md` | Map of Content - locked trip site for Marius's friends (Saigon, Phú Quốc, Hà Nội, 17 Dec 2026 - 2 Jan 2027) | AGENT, README | 0 |
| `workflows/README.md` | Map of Content - project-specific SOPs for vietnam-friends (none yet) | web-feature-slice | 1 |

## Health
- Dead links (0): none
- Orphans, nothing links to or names them (1): `private/NEXT.md`
