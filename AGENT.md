---
name: vietnam-friends-agent
description: Agent briefing for the vietnam-friends trip site - role, decisions, capability registry, rules
tags: [agent, briefing, vietnam-friends]
---

# Agent Briefing - Vietnam Friends

## Your Role

A Tier-0 static site under [[vibe-coder]]: a locked trip site in English for Marius's friends
Eugen, Cris and Женщени (names exactly as Marius wrote them), 17 Dec 2026 - 2 Jan 2027: Saigon,
Phú Quốc, Hà Nội, Saigon. Same structure as [[vietnam-itinerary-agent]]: itinerary, planner, map.

## How to Operate

- Decisions, build state and next steps: `private/NEXT.md` (git-ignored).
- Build: `python private/build_fragment.py` → `python tools/encrypt_private.py` (reads `FRIENDS_CODE`). Never commit `index.html` with a test-code payload; reset the block to `null` after tests.
- Restaurants are chosen with [[travel-restaurant-picks]]. Sources: [[michelin-check-2026-11-23]], [[eugen-picks-prices-pins-2026-11-23]].
- Activities: only Marius's starred places. No hotels, flights or reservations are pre-filled; the friends add their own in the page (flights and hotels questions after unlock). Airports and terminals: [[airports-terminals-2026-11-23]] feeds the `AIR` table in `index.html`.
- In-page state (localStorage): `vf-code`, `vf-trip` (stays by fixed leg index + 5 flights), `vf-plan`, `vf-custom`, `vf-asked`, `vf-tips-seen`, `vf-view`. Share link `#plan=` carries t (stays), f (flights), p (plan), c (own places).
- Reuse the vietnam-itinerary code (planner, map, encryption) by copying and adapting it; do not link the two sites at runtime.

## Capability Registry

| Capability | State | Note |
|---|---|---|
| Project scaffold | `included` | 2026-11-23 |
| Fixed legs (`LEGS`, 17 Dec - 2 Jan) + flights and hotels questions | `included` | 2026-11-23; dates not editable, friends add their 5 flights and stays |
| Airports and terminals (`AIR` table, flight times step, hotel link auto-fill) | `included` | 2026-11-23; [[airports-terminals-2026-11-23]] |
| Share link (`#plan=`) | `included` | 2026-11-23 |
| Itinerary / Planner / Map tabs | `included` | 2026-11-23; several places per slot |
| Info tab | `included` | 2026-11-23 (`private/info.html`, facts in [[info-tab-facts-2026-11-23]]) |
| Locked page (code in `.env`) | `included` | 2026-11-23; real code applied, live on GitHub Pages |
| First-visit guided tour (7 steps, every function, `?` reopens) | `included` | 2026-11-23; runs before the flight and hotel questions |
| Build tooling / bundler | `removed` | Tier 0, as vietnam-itinerary |
| Backend / accounts / payments | `absent` | Tier 2, not needed |
| Automated tests | `absent` | Throwaway Playwright checks per slice |

Surface modes: `index.html` = Operate (flights, hotels, planner) + Read (itinerary).

## Rules

- Never commit `.env`, `.tmp/` or `private/`.
- Public repo: no push without a ✅ [[security-checker]] run dated the same day. Re-encrypt with the real code (env var unset) before every commit.
- The code is 16+ random characters; never a short or guessable one.
