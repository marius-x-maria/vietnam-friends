---
name: vietnam-friends
description: Map of Content - locked trip site for Marius's friends (Saigon, Phú Quốc, Hà Nội, 17 Dec 2026 - 2 Jan 2027)
tags: [index, moc, web, vietnam-friends]
---

# Vietnam Friends

Tier-0 static trip site, English, for three friends travelling 17 Dec 2026 - 2 Jan 2027. Same structure as
[[vietnam-itinerary]] (itinerary, planner, map), with fixed cities and dates; the friends add their own flights, hotels and
places in the page. The content is encrypted behind one code.

## Map of Content

| Area | What's there |
|---|---|
| `AGENT.md` | [[vietnam-friends-agent]]: role, capability registry, rules |
| `tools/` | `encrypt_private.py`: encrypts the page content (code from `FRIENDS_CODE`) |
| `index.html` | The site; the encrypted payload sits in its PRIVATE block |
| `workflows/` | [[vietnam-friends-workflows]] |
| `knowledge-base/` | [[vietnam-friends-knowledge-base]] |
| `private/` | Git-ignored clear-text build source |
