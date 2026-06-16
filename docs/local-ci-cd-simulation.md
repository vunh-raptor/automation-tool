# Local CI/CD Simulation Guide (Windows 11 Home + WSL2 + Docker Desktop)

This guide shows how to **reproduce the production CI/CD pipeline on a Windows 11
Home laptop** so you can build, test, and verify **each stage**
(`verify` → `build` → `deploy`) before touching any Home Credit infrastructure.

It is written specifically for the setup you already have:

> **Windows 11 Home**, with **WSL2** enabled and the **Virtual Machine Platform**
> ("hypervisor for WSL2") turned on, running **Docker Desktop** on the **WSL2
> backend**.

That combination is fully supported and is all you need. You do **not** need
Windows Pro, Hyper‑V Manager, or a separate Linux VM (Multipass/VirtualBox) —
**WSL2 *is* your Linux box**, and Docker Desktop's WSL2 backend reuses the exact
hypervisor (Virtual Machine Platform) you already enabled.

The production design lives in the `Console log` notes file. There the pipeline:

1. runs on a **self-hosted GitLab** (`git.homecredit.net`) with a **self-managed
   runner** (`vn-small`),
2. builds a Docker image with **Docker-in-Docker (DinD)** and pushes it to an
   **external registry** (`registry.homecredit.vn`),
3. deploys via **GitOps**: it commits a new image tag into a separate
   *environments* repo, which a GitOps controller (ArgoCD/Flux) reconciles into
   the `nprod-green` Kubernetes cluster, where secrets come from **Vault**.

We can simulate all of that locally with free, open-source tools, entirely inside
WSL2.

---

## Table of contents

- [0. Where do I type these commands?](#0-where-do-i-type-these-commands)
- [1. What we are simulating (prod → local mapping)](#1-what-we-are-simulating-prod--local-mapping)
- [2. Pick a track](#2-pick-a-track)
- [3. Host prerequisites (Windows 11 Home + WSL2)](#3-host-prerequisites-windows-11-home--wsl2)
- [4. Lab architecture](#4-lab-architecture)
- [5. Track A — component-by-component (recommended first)](#5-track-a--component-by-component-recommended-first)
  - [5.1 Stage `verify`](#51-stage-verify)
  - [5.2 Stage `build` (DinD → local registry)](#52-stage-build-dind--local-registry)
  - [5.3 Stage `deploy` (GitOps → local Kubernetes)](#53-stage-deploy-gitops--local-kubernetes)
  - [5.4 Secrets (simulating Vault)](#54-secrets-simulating-vault)
- [6. Track B — full self-hosted GitLab rehearsal](#6-track-b--full-self-hosted-gitlab-rehearsal)
- [7. Per-stage verification checklist](#7-per-stage-verification-checklist)
- [8. Troubleshooting (WSL2 / Docker Desktop)](#8-troubleshooting-wsl2--docker-desktop)
- [9. Teardown](#9-teardown)
- [10. From lab to production](#10-from-lab-to-production)

---

## 0. Where do I type these commands?

Two different shells are involved. Getting this right avoids 90% of the confusion:

| Shell | When to use it | How to open |
| --- | --- | --- |
| **WSL2 (Ubuntu) bash** | **Almost everything** — `docker`, `kind`, `kubectl`, `git`, and all `simulation/scripts/*.sh`. | Start menu → "Ubuntu", or run `wsl` from any terminal. |
| **Windows PowerShell (elevated)** | Only Windows-host chores: editing the Windows `hosts` file, writing `.wslconfig`. | Start menu → "PowerShell" → **Run as administrator**. |

> 🔑 Rule of thumb: if a command starts with `docker`, `kind`, `kubectl`, `git`,
> or `./simulation/...`, run it **inside WSL2**. Clone this repo **inside the
> WSL2 filesystem** (e.g. `~/sd-automation-hub`), not under `/mnt/c/...` — the
> Linux filesystem is far faster and avoids file-permission surprises.

---

## 1. What we are simulating (prod → local mapping)

| Production component | Local stand-in | Why this is faithful enough |
| --- | --- | --- |
| Self-hosted GitLab `git.homecredit.net` | `gitlab/gitlab-ee` container (Omnibus) in WSL2 | Same software, same CI engine, same `.gitlab-ci.yml`. |
| Self-managed runner `vn-small` | `gitlab/gitlab-runner` container (docker executor, privileged) | Same executor + DinD model as prod. |
| External registry `registry.homecredit.vn` | `registry:2` container on `localhost:5000` | A standalone registry (not GitLab's built-in) — mirrors the "external registry + service account" design. |
| Base-image registry `registry.vn.eit.zone` | Docker Hub (`docker:24.0.5`, `docker:24.0.5-dind`) | We just pull the same tool images directly. |
| `nprod-green` Kubernetes cluster | `kind` (Kubernetes-in-Docker) on Docker Desktop | A real, conformant K8s API to deploy into. |
| GitOps controller (ArgoCD/Flux) | ArgoCD installed in the local cluster | Same pull-based reconcile loop. |
| Environments repo (`.../nprod-green/...`) | A second project in local GitLab (Track B) or a local git repo (Track A) | Same "commit a tag → controller deploys" flow. |
| Vault secret injection | a plain K8s `Secret` (or `hashicorp/vault` dev mode) | Proves the app reads secrets from the platform, not from a baked-in `.env`. |
| Corporate proxy | omitted locally | The proxy only matters inside the HC network. |
| LDAP / JIRA / SSO backends (`.env.example`) | dummy values / optional mock | Not needed to verify the *pipeline*; only the app's runtime features. |

---

## 2. Pick a track

There are two ways to use this guide. **Start with Track A.**

- **Track A — component simulation (recommended, lighter).** Test each stage in
  isolation with the smallest toolset. No self-hosted GitLab required. Fastest
  way to prove the *logic* of each stage. Runs comfortably on a laptop with
  Docker Desktop + WSL2.

- **Track B — full rehearsal (heavier).** Stand up a real self-hosted GitLab +
  runner inside WSL2 and run the actual `.gitlab-ci.yml` end to end. Highest
  fidelity, but GitLab alone wants ~4 GB RAM — give WSL2 the headroom first (see
  [§3](#3-host-prerequisites-windows-11-home--wsl2)).

Both tracks use the same lab files in [`simulation/`](../simulation).

---

## 3. Host prerequisites (Windows 11 Home + WSL2)

### 3.1 Confirm WSL2 + the hypervisor are on

You said these are already enabled — confirm in an **elevated PowerShell**:

```powershell
wsl --status          # "Default Version: 2"
wsl --list --verbose  # your distro should show VERSION 2 and STATE Running/Stopped
```

If `wsl --status` complains, enable the two Windows features (this is the
"hypervisor for WSL2"), then reboot:

```powershell
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
wsl --set-default-version 2
```

> Windows 11 **Home** does not ship Hyper‑V Manager — and you don't need it.
> WSL2 (and Docker Desktop's WSL2 backend) run on the **Virtual Machine
> Platform**, which Home fully supports.

Install a Linux distro if you don't have one yet (Ubuntu is a safe default):

```powershell
wsl --install -d Ubuntu
```

### 3.2 Docker Desktop with the WSL2 backend

1. Install **Docker Desktop for Windows**.
2. **Settings → General →** tick **"Use the WSL 2 based engine"**.
3. **Settings → Resources → WSL Integration →** enable integration for your
   distro (e.g. Ubuntu).
4. Apply & Restart. Then, **inside WSL2**, confirm the CLI talks to the daemon:

```bash
docker version        # Client + Server both reported
docker run --rm hello-world
```

### 3.3 Tools inside WSL2

Run these **inside the WSL2 distro**:

```bash
# kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl && rm kubectl

# kind (Kubernetes-in-Docker)
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.23.0/kind-linux-amd64
sudo install -o root -g root -m 0755 kind /usr/local/bin/kind && rm ./kind

# git is preinstalled on Ubuntu; python3 is only needed for the LOCAL verify path
kubectl version --client
kind version
```

### 3.4 (Track B only) Give WSL2 enough RAM

Self-hosted GitLab needs ~4 GB. Copy the sample
[`simulation/wsl/.wslconfig.example`](../simulation/wsl/.wslconfig.example) to
`C:\Users\<you>\.wslconfig` (Windows side), then from an elevated PowerShell:

```powershell
wsl --shutdown      # restart WSL2 so the new limits apply
```

Restart Docker Desktop afterwards. Track A does **not** need this.

**Sizing summary**

| Track | RAM (free) for WSL2 | Disk |
| --- | --- | --- |
| A (components) | 4–6 GB | 20 GB |
| B (full GitLab) | 8 GB | 40 GB |

---

## 4. Lab architecture

```
   Windows 11 Home  ──►  WSL2 (Virtual Machine Platform)  ──►  Docker Desktop engine
 ┌───────────────────────────────────────────────────────────────────┐
 │                                                                     │
 │  TRACK B only                              ALL TRACKS               │
 │  ┌────────────────┐  ┌────────────────┐   ┌────────────────────┐    │
 │  │ gitlab-ee      │  │ gitlab-runner  │   │ registry:2         │    │
 │  │ (UI :8080)     │◄─┤ docker executor│   │ localhost:5000     │    │
 │  │ git + CI       │  │ privileged+DinD│──►│ (external registry │    │
 │  └────────────────┘  └───────┬────────┘   │  stand-in)         │    │
 │          ▲                   │ docker build/push                    │
 │          │ git push tag      ▼            └─────────┬──────────┘    │
 │          │            ┌──────────────┐              │ image          │
 │          └────────────┤ build job    │              │                │
 │                       │ (DinD)       │              ▼                │
 │                       └──────────────┘    ┌────────────────────┐    │
 │  env repo (commit new tag) ───────────────►│ kind cluster      │    │
 │                                            │  ┌──────────────┐  │    │
 │                                            │  │ ArgoCD       │  │    │
 │                                            │  │ (reconciles) │  │    │
 │                                            │  └──────┬───────┘  │    │
 │                                            │         ▼          │    │
 │                                            │  Deployment        │    │
 │                                            │  sd-automation-hub │    │
 │                                            │  :8501 /_stcore/health │
 │                                            └────────────────────┘    │
 └───────────────────────────────────────────────────────────────────┘
   Published container ports (5000, 8080, 8501) are forwarded by Docker
   Desktop to Windows `localhost`, so they work from both WSL2 and your
   Windows browser.
```

In **Track A** you drive the boxes by hand (plain `docker`, `git`, `kubectl`,
`argocd`). In **Track B** GitLab + the runner drive them exactly like prod.

---

## 5. Track A — component-by-component (recommended first)

This track proves each pipeline stage **without** GitLab, so you can iterate fast.
Each stage maps to one helper script in [`simulation/scripts/`](../simulation/scripts).

> Run everything **inside WSL2**, from the repo root, unless noted.

### 5.1 Stage `verify`

**What prod does:** install deps, check Streamlit, byte-compile the entrypoint.

**Simulate it** — by default the script runs in the **exact `python:3.12`
container the CI uses**, so you don't depend on whatever Python ships in your
distro:

```bash
./simulation/scripts/stage1-verify.sh
# ...or run against your WSL2 host's own python3:
LOCAL=1 ./simulation/scripts/stage1-verify.sh
```

**Verify:** the script exits `0` and prints the Streamlit version. A non-zero
exit means a dependency or syntax error — exactly what the prod `verify` stage
would catch.

### 5.2 Stage `build` (DinD → local registry)

**What prod does:** build the image inside DinD, push to `registry.homecredit.vn`.

**Simulate it** with a local registry. We use `localhost:5000` on purpose:
Docker treats `localhost` registries as **insecure by default**, so there is
**no daemon config to edit** on Docker Desktop.

```bash
# 1) start a standalone registry (our 'registry.homecredit.vn' stand-in)
docker run -d --name lab-registry -p 5000:5000 registry:2

# 2) build the app image and push it (the script does both)
./simulation/scripts/stage2-build.sh v0.0.1
```

`stage2-build.sh` runs the same commands as the `build-app` job:

```bash
IMAGE="localhost:5000/service_desk/sd-automation-hub:${1:-v0.0.1}"
docker build --build-arg BUILD_VERSION="${1:-v0.0.1}" -t "$IMAGE" .
docker push "$IMAGE"
```

**Verify** the image really landed in the registry (works from WSL2 *or* a
Windows browser, thanks to Docker Desktop's localhost forwarding):

```bash
curl -s http://localhost:5000/v2/_catalog
# => {"repositories":["service_desk/sd-automation-hub"]}
curl -s http://localhost:5000/v2/service_desk/sd-automation-hub/tags/list
# => {"name":"...","tags":["v0.0.1"]}
```

> This is the fastest way to debug the `Dockerfile` itself (proxy args, Chromium
> install, non-root user, healthcheck) independently of CI.

### 5.3 Stage `deploy` (GitOps → local Kubernetes)

**What prod does:** commit a new image tag into the env repo; ArgoCD syncs it to
the cluster.

```bash
# 1) create a local cluster (stands in for nprod-green)
kind create cluster --name sdah --config simulation/kind/kind-cluster.yaml

# 2) make the built image available to the cluster (sideload — no registry pull).
#    This is why localhost:5000 vs registry.local:5000 doesn't matter in Track A.
kind load docker-image localhost:5000/service_desk/sd-automation-hub:v0.0.1 --name sdah

# 3) create the secret the Deployment expects (see 5.4)
kubectl create secret generic sd-automation-hub-secrets --from-env-file=.env.example
```

**Quick path — verify the app actually runs.** Apply the manifest directly; this
is exactly what the controller does after a sync:

```bash
cp simulation/k8s/deployment.yml /tmp/deployment.yml
sed -i "s|:v0.0.0|:v0.0.1|" /tmp/deployment.yml       # point at the tag you loaded
kubectl apply -f /tmp/deployment.yml
kubectl rollout status deploy/sd-automation-hub
curl -fsS http://localhost:8501/_stcore/health        # => ok (NodePort mapped by kind)
```

Then open <http://localhost:8501> in your **Windows browser** — Docker Desktop
forwards the port out of WSL2 for you.

**Faithful path — verify the GitOps loop itself.** ArgoCD must reach the env repo
from *inside* the cluster, so host it on a reachable git server (a GitHub repo, or
the Track B GitLab) — a `/tmp` folder will **not** work:

```bash
# a) create an env repo on a reachable git host, with this layout on branch
#    sd-automation-hub-release:
#        sd-automation-hub/deployment.yml   (copy of simulation/k8s/deployment.yml)

# b) install ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl -n argocd rollout status deploy/argocd-server

# c) edit repoURL in simulation/argocd/application.yaml, then apply it
kubectl apply -f simulation/argocd/application.yaml

# d) reproduce the deploy-app job: clone the env repo, bump the tag, push
git clone <your-env-repo-url> /tmp/env
git -C /tmp/env checkout sd-automation-hub-release
./simulation/scripts/stage3-deploy.sh v0.0.1 /tmp/env
```

**Verify** the rollout:

```bash
kubectl get applications -n argocd          # (faithful path) SYNCED / HEALTHY
kubectl get pods                            # sd-automation-hub-... Running
curl -fsS http://localhost:8501/_stcore/health   # => ok
```

### 5.4 Secrets (simulating Vault)

Production injects secrets from Vault (provisioned via `spiral-scheme`). Two
fidelity levels:

**Minimum (recommended for the lab) — a plain K8s Secret:**

```bash
kubectl create secret generic sd-automation-hub-secrets \
  --from-env-file=.env.example
```

The sample `deployment.yml` already references it via `envFrom: secretRef`. This
proves the app reads its config from the platform, not from a committed `.env`.

**Stretch — real Vault dev server:**

```bash
docker run -d --name lab-vault -p 8200:8200 \
  -e VAULT_DEV_ROOT_TOKEN_ID=root hashicorp/vault
export VAULT_ADDR=http://localhost:8200 VAULT_TOKEN=root
vault kv put secret/sd-automation-hub LDAP_URL=ldap://example OTP_SECRET=demo
```

Wiring Vault → pods requires the Vault Agent Injector (a Helm install). That is
overkill for verifying the pipeline; use it only if you specifically want to
rehearse the Vault integration.

---

## 6. Track B — full self-hosted GitLab rehearsal

This runs the **actual `.gitlab-ci.yml`** through a real GitLab + runner, so the
trigger model (`only: tags`), variables, and stages behave exactly like prod.

> Do [§3.4](#34-track-b-only-give-wsl2-enough-ram) first — GitLab will thrash
> without ~4 GB free in WSL2.

### 6.1 Resolve the lab hostnames (both sides)

Track B uses the names `gitlab.local` and `registry.local`. They must resolve in
**two** places:

1. **Windows** (so your browser can open the GitLab UI). In an **elevated
   PowerShell**, run the helper:

   ```powershell
   .\simulation\scripts\win-hosts-setup.ps1
   ```

   (It appends `127.0.0.1 gitlab.local registry.local` to
   `C:\Windows\System32\drivers\etc\hosts`.)

2. **WSL2** (so `git push` from your distro resolves the name). Inside WSL2:

   ```bash
   echo "127.0.0.1 gitlab.local registry.local" | sudo tee -a /etc/hosts
   ```

Also mark the lab registry insecure for the Docker Desktop engine —
**Settings → Docker Engine**, add `registry.local:5000`, then **Apply &
Restart**:

```json
{ "insecure-registries": ["registry.local:5000"] }
```

> On the Docker Desktop WSL2 backend the daemon lives in the `docker-desktop`
> distro, **not** your Ubuntu distro — so editing `/etc/docker/daemon.json`
> inside Ubuntu has no effect. Use the Settings UI above.

### 6.2 Start GitLab + runner + registry

```bash
cd simulation
docker compose -f docker-compose.lab.yml up -d
# GitLab takes 3–5 min to initialise. Watch for "Reconfigured!":
docker compose -f docker-compose.lab.yml logs -f gitlab | grep -i reconfigured
```

Get the root password and log in at <http://gitlab.local:8080> (user `root`):

```bash
docker compose -f docker-compose.lab.yml exec gitlab \
  cat /etc/gitlab/initial_root_password
```

### 6.3 Create the two projects

In the GitLab UI create:

1. `sd-automation-hub` — push **this** repo into it.
2. `sd-automation-hub-env` — the environments repo; add
   `sd-automation-hub/deployment.yml` on a branch named `sd-automation-hub-release`.

```bash
git remote add lab http://root@gitlab.local:8080/root/sd-automation-hub.git
git push lab HEAD:main
```

### 6.4 Register the runner with DinD

In GitLab: **Admin → CI/CD → Runners → New instance runner**, copy the
authentication token (`glrt-...`), then:

```bash
docker compose -f docker-compose.lab.yml exec runner gitlab-runner register \
  --non-interactive \
  --url http://gitlab.local:8080 \
  --token "glrt-XXXXXXXX" \
  --executor docker \
  --docker-image docker:24.0.5 \
  --docker-privileged \
  --run-untagged="true" \
  --docker-volumes /certs/client \
  --docker-network-mode sdah-lab_lab
```

- `--docker-privileged` → required so the **DinD** service container can run a
  nested daemon.
- `--docker-network-mode sdah-lab_lab` → puts job containers on the lab network
  so they can reach `registry.local:5000` and `gitlab.local`.

### 6.5 Set CI/CD variables

In the `sd-automation-hub` project → **Settings → CI/CD → Variables**:

| Key | Value (lab) | Flags |
| --- | --- | --- |
| `REGISTRY_USER` | `lab` | masked |
| `REGISTRY_PASSWORD` | `lab` | masked |
| `GITLAB_PF_TOKEN` | a project token with `write_repository` on the env repo | masked, protected |

Also protect the tag pattern `v*` under **Settings → Repository → Protected tags**
so protected variables are available to tag pipelines.

### 6.6 Use the lab pipeline and run it

The lab pipeline [`simulation/.gitlab-ci.lab.yml`](../simulation/.gitlab-ci.lab.yml)
is the production pipeline with two lab-only tweaks: it points at
`registry.local:5000` and disables DinD TLS + allows the insecure local registry.
Copy it in as `.gitlab-ci.yml` for the rehearsal, then trigger a release:

```bash
git tag -a v0.0.1 -m "lab release"
git push lab v0.0.1
```

Watch **CI/CD → Pipelines**: you should see `verify → build → deploy` run in
order, the image appear in the local registry, and a commit land on the env
repo's `sd-automation-hub-release` branch — which your ArgoCD (from Track A §5.3)
then deploys.

---

## 7. Per-stage verification checklist

| Stage | "Green" looks like | Command to confirm |
| --- | --- | --- |
| `verify` | exit 0, prints Streamlit version | `./simulation/scripts/stage1-verify.sh` |
| `build` | image + tag exist in the registry | `curl -s localhost:5000/v2/_catalog` |
| `deploy` (commit) | env repo has a new commit bumping the tag | `git -C /tmp/env log --oneline -1` |
| `deploy` (sync) | ArgoCD app `Synced` + `Healthy` | `kubectl get applications -n argocd` |
| runtime | pod `Running`, healthcheck `ok` | `kubectl get pods` + `curl .../_stcore/health` |

---

## 8. Troubleshooting (WSL2 / Docker Desktop)

- **`docker: command not found` inside WSL2.** Docker Desktop → **Settings →
  Resources → WSL Integration** isn't enabled for this distro. Enable it, then
  **Apply & Restart**.
- **Everything is slow / files are weird.** You cloned under `/mnt/c/...`. Move
  the repo into the Linux filesystem (`~/sd-automation-hub`) and re-run.
- **GitLab is slow / unhealthy on boot.** Give WSL2 4 GB+ (`.wslconfig`, see
  §3.4) and wait ~5 minutes. The container is unhealthy until reconfigure
  finishes — that's normal.
- **Runner job: "Cannot connect to the Docker daemon".** The runner needs
  `--docker-privileged`; the build job needs matching `DOCKER_HOST` /
  `DOCKER_TLS_CERTDIR`. The lab pipeline disables TLS (`DOCKER_TLS_CERTDIR=""`,
  `DOCKER_HOST=tcp://docker:2375`) to keep it simple.
- **`docker push` → "http: server gave HTTP response to HTTPS client".** Use
  `localhost:5000` in Track A (auto-insecure). For Track B's `registry.local:5000`,
  add it under **Settings → Docker Engine → insecure-registries** and restart —
  editing `/etc/docker/daemon.json` in Ubuntu does nothing on the WSL2 backend.
- **kind pod stuck `ImagePullBackOff`.** Easiest fix: `kind load docker-image <img>`
  and keep `imagePullPolicy: IfNotPresent` (already set in the sample manifest).
- **`localhost:8501` doesn't open in the Windows browser.** Confirm the kind
  cluster came up with `simulation/kind/kind-cluster.yaml` (it maps the NodePort
  to host `8501`) and the pod is `Running`. Docker Desktop forwards the port to
  Windows automatically.
- **Job containers can't resolve `gitlab.local` / `registry.local`.** Register the
  runner with `--docker-network-mode sdah-lab_lab` (the compose network name).
- **ArgoCD won't sync.** Confirm `repoURL`, `targetRevision: sd-automation-hub-release`,
  and `path: sd-automation-hub` in the Application match your env repo.

---

## 9. Teardown

```bash
# Track A (run inside WSL2)
docker rm -f lab-registry lab-vault 2>/dev/null
kind delete cluster --name sdah
rm -rf /tmp/env

# Track B
cd simulation && docker compose -f docker-compose.lab.yml down -v
```

`-v` removes the GitLab/registry volumes too — omit it if you want to keep state
between sessions. To reclaim the WSL2 disk image afterwards, run
`wsl --shutdown` then optionally `docker system prune` inside WSL2.

---

## 10. From lab to production

When the lab is green, here's exactly what changes for the real Home Credit run
(nothing structural — only endpoints, auth, and TLS):

| Lab | Production |
| --- | --- |
| `localhost:5000` / `registry.local:5000`, no auth, HTTP | `registry.homecredit.vn`, **service account**, TLS |
| DinD TLS disabled | DinD TLS **enabled** (`DOCKER_TLS_CERTDIR=/certs`) |
| Docker Hub base images | `registry.vn.eit.zone/external/...` |
| no proxy | corporate `http_proxy` / `https_proxy` / `no_proxy` |
| `kind` cluster | `nprod-green` cluster (ArgoCD already platform-managed) |
| plain K8s `Secret` | **Vault** injection (provisioned via `spiral-scheme`) |
| local runner | `vn-small` self-managed runner |
| local git env repo | `.../environments/vn/nprod-green/sd-automation-hub` |

Do the onboarding (`app_code`, `apps-registry`, `spiral-scheme`) and request the
registry service account **in parallel** with this lab work — see the build/deploy
runbook for those organizational steps.

> ⚠️ Reminder from `CHANGES.md`: the app still has three Windows-only components
> (Outlook COM email, PowerShell CyberArk, a Windows file-share DB path) that
> must be refactored for Linux before the *deployed* app is fully functional. The
> pipeline will build and deploy regardless; those features just won't run until
> refactored. (Ironically, those bits are happiest on the very Windows host
> you're reading this on — the lab just proves the *pipeline*, not those Windows
> integrations.)
