# Docker 201: From Inner Loop to Production-Ready

The demo repo from the Docker 201 webinar (July 9, 2026). Everything we ran live, ready for you to run yourself.

The arc is simple: build and run the app the way you already do, harden the image with a Docker Hardened Image, analyze both with Docker Scout to see the difference, then hand the whole repo to an AI coding agent inside a Docker Sandbox and review its work safely.

## What you need

- Docker Desktop installed ([docker.com/get-started](https://www.docker.com/get-started/))
- That's it. Everything else runs in containers.

## 1. Build and run (the inner loop)

```bash
docker compose up --build
```

Open http://localhost:8000. You built and ran that. Check out `/inventory` and `/health` for the API side.

This is the loop you know: change the code, rebuild, see it live in seconds.

## 2. Look inside the image

The app runs. But what's actually in the image you just built?

```bash
docker scout quickview docker-201-demo-demo
```

Then get the full CVE picture:

```bash
docker scout cves docker-201-demo-demo
```

Take note of the total count, the criticals and highs, and which packages carry them. Most of what you see didn't come from the app. It came with the base image.

## 3. Swap to a hardened base

Open `Dockerfile.hardened`. Same app, hardened foundation. Because Docker Hardened Images are minimal (no pip, no package manager in the runtime image), dependencies are installed in the `-dev` variant and copied into the minimal runtime image that Docker builds, patches, and signs.

Build and run it:

```bash
docker compose --profile hardened up --build demo-hardened
```

The hardened variant serves on http://localhost:8001. Same app, same page, same behavior.

## 4. Scan it again and compare

```bash
docker scout cves docker-201-demo-demo-hardened
```

Compare against the standard image from step 2. Fewer packages, a fraction of the vulnerabilities, roughly half the size. You didn't change your app. You changed what you build on.

## Demo 2: hand it to an agent, safely

Everything above hardened and analyzed the app. This part shows the other half of a production-ready workflow in 2026: letting an AI coding agent work on this repo without giving it your machine.

Docker Sandboxes run coding agents in an isolated microVM with their own kernel, Docker daemon, filesystem, and network, and no path back to your host. See [SANDBOXES.md](SANDBOXES.md) for the full walkthrough. The short version:

```bash
# one-time setup (macOS)
brew install docker/tap/sbx
sbx login                       # pick the Balanced network policy

# from this repo, hand it to an agent on its own branch
sbx run claude --clone
```

Give the agent a small task, for example: "add a `/version` endpoint that returns the app version and variant." While it works, in a second terminal:

```bash
sbx ls                          # what's running
sbx policy ls                   # what it's allowed to reach
```

When it finishes, review the work like a pull request. It never touched your working tree:

```bash
git status                      # your repo stays clean
cd <that path>
sbx exec <sandbox> git diff     # read every line before you trust it
```

Keep it (`git push`) or throw it away (`sbx rm claude-docker-201-demo`). Your call.

## 5. Try it on your own project

- Pick one service you own and run `docker scout quickview` on its image.
- Find a hardened base that matches your stack in the Docker Hardened Images catalog.
- Swap your base image in a branch (multi-stage if your runtime needs dependencies installed), rebuild, re-analyze, compare.
- Install the `sbx` CLI and run an agent on a repo you own with `sbx run claude --clone`, then review the diff with `sbx exec <sandbox> git diff`.

## Resources

- Session recording and slides: sent to all registrants
- [Docker Scout docs](https://docs.docker.com/scout/)
- [Docker Hardened Images docs](https://docs.docker.com/dhi/)
- [Docker Sandboxes docs](https://docs.docker.com/ai/sandboxes/)
- Want help rolling this out? [Request onboarding support](https://www.docker.com/onboarding-request/)

Questions? Reach out to the Docker Onboarding team.
