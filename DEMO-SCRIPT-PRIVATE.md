# Demo run-of-show (private, not for the public repo)

Keep this file out of the published repo (it's in .gitignore-worthy territory, but if it ships it's harmless). Your script for the two live demos on July 9.

## Pre-flight (morning of July 9)

- [ ] Clean slate: fresh clone into ~/dev, `docker system prune` if needed
- [ ] Build both images with `--no-cache`, confirm both run (8000 amber, 8001 green)
- [ ] Run both Scout analyses, write down the fresh counts (they drift), patch slide 8 amber card and the notes on slides 5/7/8 if needed
- [ ] Sandboxes: confirm the agent image is cached (`sbx run claude --clone` in a throwaway dir, let it start, `sbx rm`). Re-warm if the laptop rebooted.
- [ ] Second terminal ready at the repo root for `sbx ls` / `sbx policy ls`
- [ ] Browser tab on docker.com/onboarding-request for the slide 14 tour; feedback form link staged for chat
- [ ] Share the ENTIRE screen, not a window. Terminal font up, notifications off.

## Demo 1: Harden It. Prove It. (slide 8, ~12 min)

1. App already running from the standard image (`docker compose up` before going live). Open localhost:8000, point at the amber badge.
2. Open `Dockerfile`, point at `FROM python:3.14-slim`: "perfectly normal, works fine, and carrying 133 packages."
3. Open `Dockerfile.hardened` side by side: deps in the -dev variant, copied into the minimal runtime. "The runtime doesn't even have pip. That's the feature." Mention the same-libc-family rule.
4. Build live: `docker compose --profile hardened up --build demo-hardened`. While it builds, talk the amber card (56->26 MB, 133->45 packages). No CVE numbers yet.
5. Open localhost:8001 next to 8000: same page, green badge. "Same app, new foundation."
6. Analyze standard: `docker scout cves docker-201-demo-demo`. 35 total. The perl moment: point at the critical, "not fixed." Slow down.
7. Analyze hardened: `docker scout cves docker-201-demo-demo-hardened`. Zero. Pause. Then the two honest footnotes (zero isn't a force field; VEX).

Fallback: hardened image pre-built this morning, so if the live build stalls, `docker compose --profile hardened up -d demo-hardened` and continue at step 5. If Scout hangs, use the morning screenshots.

Bridge line into Part 2: "for two sessions the person writing this code was you. That's not the whole story anymore. Is what's building it trustworthy?"

## Demo 2: An Agent, Contained (slide 11, ~7 min)

1. Same repo. `sbx run claude --clone`. Narrate: microVM booting with its own everything, clone flag mounts your repo read-only so the agent works on a private clone.
2. Task to the agent: "Add a `/version` endpoint that returns the app version and variant as JSON."
3. Second terminal while it works: `sbx ls`, then `sbx policy ls`. This is the "read the policy, don't trust me" beat. Say the credentials-never-inside line here.
4. Session ends, exit the agent. Sandbox persists but is contained.
5. Review: `git status` (clean), then `sbx exec claude-docker-201-demo git diff`. Read the diff. "Zero host access, zero credentials inside, one clean diff. My call."

Fallback: if the agent is slow, keep narrating `sbx ls` / `sbx policy ls`, that filler IS the governance content. If it stalls hard, cut to screenshots and walk the same five beats. The slide 11 amber card carries the 0/0/1 result regardless.

Reset between rehearsal and showtime: `sbx rm claude-docker-201-demo` (keeps the image cached, clears the sandbox).

## Timing

Demo 1 target: 12 min (green badge ~18:00 on session clock, perl ~21:00, zero ~23:00). Demo 2 target: 7 min (agent working by ~30:00, diff review by ~34:00). If Demo 1 runs long, compress the Demo 2 governance narration, not the diff review.
