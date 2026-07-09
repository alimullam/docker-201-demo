# Docker Sandboxes: run an AI agent on this repo, safely

This is the Demo 2 walkthrough from the Docker 201 webinar. It shows how to hand this repository to an AI coding agent without giving the agent access to your host machine, your credentials, or your main working tree.

Docker Sandboxes run each agent session inside a dedicated microVM: its own kernel, its own Docker daemon, its own filesystem, its own network, and no path back to your host. Credentials stay in your host keychain and are injected by a proxy, so they are never written inside the sandbox. Docker Sandboxes is experimental and under active development.

## Prerequisites

- macOS Sonoma (14) or later on Apple silicon, or Windows 11 with the Hypervisor Platform enabled, or Ubuntu 24.04+ with KVM.
- Docker Desktop is not required for the `sbx` CLI.
- An agent and its auth. This guide uses Claude Code: either a Claude subscription (sign in with `/login` inside the sandbox) or an API key (`sbx secret set -g anthropic`).

## One-time setup

```bash
# macOS
brew install docker/tap/sbx
sbx login
```

On first login you choose a default network policy. Pick **Balanced**: it allows common development services and blocks everything else. You can allow-list specific hosts later.

## Run an agent on this repo

From the repo root:

```bash
sbx run claude --clone
```

`--clone` mounts your repository read-only and gives the agent a private clone inside the sandbox. The agent works on the clone, so your real working tree is never touched.

Give it a small, real task. The one used in the webinar:

> Add a `/version` endpoint to the Flask app that returns the app version and the variant name as JSON.

## Watch the governance while it works

In a second terminal:

```bash
sbx ls           # the sandbox, the agent, its status, the workspace
sbx policy ls    # exactly what the agent is allowed to reach
```

Two things worth saying out loud: the containers the agent builds run on the sandbox's own Docker daemon and never appear in your host `docker ps`, and your API key is never inside the sandbox, a host-side proxy injects it into outbound calls.

## Review the agent's work like a pull request

When the session ends:

```bash
git status                    # your repo: clean, nothing changed
sbx exec <sandbox> git diff   # read every line before you trust it
```

If you like it, push and open a PR:

```bash
# keep it: fetch the sandbox-<name> git remote, then merge or open a PR
gh pr create
```

If you don't, throw the whole thing away. Your main working tree never changed:

```bash
sbx rm claude-docker-201-demo
```

## Useful commands

| Command | What it does |
|---|---|
| `sbx ls` | List sandboxes, status, and workspace |
| `sbx policy ls` | Show the active network policy |
| `sbx policy allow network -g <host>` | Allow the agent to reach a specific host |
| `sbx exec -it <sandbox> bash` | Open a shell inside the sandbox to inspect it |
| `sbx stop <sandbox>` | Pause a sandbox without deleting it |
| `sbx rm <sandbox>` | Delete the sandbox, its clone, and everything inside |

## A stronger boundary: clone mode

With `--clone`, your repository is mounted read-only and the agent works on a private clone inside the VM. Its edits reach you only when you explicitly review them with `sbx exec <sandbox> git diff` and fetch the `sandbox-<name>` git remote. The agent can never modify your host repo directly.

## Learn more

- [Docker Sandboxes docs](https://docs.docker.com/ai/sandboxes/)
- [Get started guide](https://docs.docker.com/ai/sandboxes/get-started/)
- [Security and isolation](https://docs.docker.com/ai/sandboxes/security/)
- Feedback (it is experimental, they want it): [github.com/docker/sbx-releases/issues](https://github.com/docker/sbx-releases/issues)
