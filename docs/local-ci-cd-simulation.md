# Local CI/CD Simulation Guide

This guide shows how to **reproduce the production CI/CD pipeline on your own
machine** so you can build, test, and verify **each stage** (`verify` → `build`
→ `deploy`) before touching any Home Credit infrastructure.

The production design lives in the `Console log` notes file. There the pipeline:

1. runs on a **self-hosted GitLab** (`git.homecredit.net`) with a **self-managed
   runner** (`vn-small`),
2. builds a Docker image with **Docker-in-Docker (DinD)** and pushes it to an
   **external registry** (`registry.homecredit.vn`),
3. deploys via **GitOps**: it commits a new image tag into a separate
   *environments* repo, which a GitOps controller (ArgoCD/Flux) reconciles into
   the `nprod-green` Kubernetes cluster, where secrets come from **Vault**.

We can simulate all of that locally with free, open-source tools.

---

## Table of contents

- [1. What we are simulating (prod → local mapping)](#1-what-we-are-simulating-prod--local-mapping)
- [2. Pick a track](#2-pick-a-track)
- [3. Host prerequisites](#3-host-prerequisites)
- [4. Lab architecture](#4-lab-architecture)
- [5. Track A — component-by-component (recommended first)](#5-track-a--component-by-component-recommended-first)
  - [5.1 Stage `verify`](#51-stage-verify)
  - [5.2 Stage `build` (DinD → local registry)](#52-stage-build-dind--local-registry)
  - [5.3 Stage `deploy` (GitOps → local Kubernetes)](#53-stage-deploy-gitops--local-kubernetes)
  - [5.4 Secrets (simulating Vault)](#54-secrets-simulating-vault)
- [6. Track B — full self-hosted GitLab rehearsal](#6-track-b--full-self-hosted-gitlab-rehearsal)
- [7. Per-stage verification checklist](#7-per-stage-verification-checklist)
- [8. Troubleshooting](#8-troubleshooting)
- [9. Teardown](#9-teardown)
- [10. From lab to production](#10-from-lab-to-production)

---

## 1. What we are simulating (prod → local mapping)

| Production component | Local stand-in | Why this is faithful enough |
| --- | --- | --- |
| Self-hosted GitLab `git.homecredit.net` | `gitlab/gitlab-ee` container (Omnibus) | Same software, same CI engine, same `.gitlab-ci.yml`. |
| Self-managed runner `vn-small` | `gitlab/gitlab-runner` container (docker executor, privileged) | Same executor + DinD model as prod. |
| External registry `registry.homecredit.vn` | `registry:2` container on `localhost:5000` | A standalone registry (not GitLab's built-in) — mirrors the "external registry + service account" design. |
| Base-image registry `registry.vn.eit.zone` | Docker Hub (`docker:24.0.5`, `docker:24.0.5-dind`) | We just pull the same tool images directly. |
| `nprod-green` Kubernetes cluster | `kind` (Kubernetes-in-Docker) or `k3d` | A real, conformant K8s API to deploy into. |
| GitOps controller (ArgoCD/Flux) | ArgoCD installed in the local cluster | Same pull-based reconcile loop. |
| Environments repo (`.../nprod-green/...`) | A second project in local GitLab (Track B) or a local git repo (Track A) | Same "commit a tag → controller deploys" flow. |
| Vault secret injection | `hashicorp/vault` dev mode, or a plain K8s `Secret` | Proves the app reads secrets from the platform, not from a baked-in `.env`. |
| Corporate proxy | omitted locally (`no_proxy` everything) | The proxy only matters inside the HC network. |
| LDAP / JIRA / SSO backends (`.env.example`) | dummy values / optional mock | Not needed to verify the *pipeline*; only the app's runtime features. |

---

## 2. Pick a track

There are two ways to use this guide. **Start with Track A.**

- **Track A — component simulation (recommended, lighter).** Test each stage in
  isolation with the smallest toolset. No self-hosted GitLab required. Fastest
  way to prove the *logic* of each stage. Runs comfortably on a laptop with
  Docker Desktop.

- **Track B — full rehearsal (heavier).** Stand up a real self-hosted GitLab +
  runner and run the actual `.gitlab-ci.yml` end to end. Highest fidelity, but
  GitLab alone wants ~4 GB RAM. Use a dedicated VM.

Both tracks use the same lab files in [`simulation/`](../simulation).

---

## 3. Host prerequisites

### Option 1 — Docker Desktop on your machine (fine for Track A)

Install:

- Docker Engine / Docker Desktop (with Compose v2)
- `kubectl`
- `kind` (https://kind.sigs.k8s.io) **or** `k3d`
- `git`
- Python 3.12 (only for the local `verify` step)

### Option 2 — A throwaway Ubuntu VM (recommended for Track B)

Track B runs many heavy services at once, so isolate it in a VM. Easiest is
[Multipass](https://multipass.run):

```bash
# 4 vCPU, 8 GB RAM, 40 GB disk — GitLab needs the headroom
multipass launch 22.04 --name sdah-lab --cpus 4 --memory 8G --disk 40G
multipass shell sdah-lab

# inside the VM:
sudo apt-get update && sudo apt-get install -y docker.io docker-compose-v2 git
sudo usermod -aG docker "$USER"   # then log out/in
# install kubectl + kind as per their docs
```

> VirtualBox/VMware/Hyper-V work too — just give the guest ≥ 8 GB RAM and enable
> nested virtualization is **not** required (everything here is containers, not
> nested VMs).

**Sizing summary**

| Track | CPU | RAM (free) | Disk |
| --- | --- | --- | --- |
| A (components) | 2+ | 4–6 GB | 20 GB |
| B (full GitLab) | 4+ | 8 GB | 40 GB |

### One-time host setup (both tracks)

So the same names resolve on the host **and** inside the Docker network, add to
`/etc/hosts`:

```
127.0.0.1 gitlab.local registry.local
```

The lab registry is plain HTTP, so mark it insecure for your local Docker daemon
(`/etc/docker/daemon.json`), then restart Docker:

```json
{ "insecure-registries": ["registry.local:5000"] }
```

> On Docker Desktop, set this under **Settings → Docker Engine** instead of
> editing the file directly.

---

## 4. Lab architecture

```
                 your machine / VM (Docker)
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
```

In **Track A** you drive the boxes by hand (plain `docker`, `git`, `kubectl`,
`argocd`). In **Track B** GitLab + the runner drive them exactly like prod.

---

## 5. Track A — component-by-component (recommended first)

This track proves each pipeline stage **without** GitLab, so you can iterate fast.
Each stage maps to one helper script in [`simulation/scripts/`](../simulation/scripts).

> Run everything from the repo root unless noted.

### 5.1 Stage `verify`

**What prod does:** install deps, check Streamlit, byte-compile the entrypoint.

**Simulate it** (this is literally the production `verify` job, run locally):

```bash
./simulation/scripts/stage1-verify.sh
# or manually:
python3.12 -m venv .venv && . .venv/bin/activate
pip install --no-cache-dir -r requirements.txt
streamlit --version
python -m py_compile main_site.py
```

**Verify:** the script exits `0` and prints the Streamlit version. A non-zero
exit means a dependency or syntax error — exactly what the prod `verify` stage
would catch.

### 5.2 Stage `build` (DinD → local registry)

**What prod does:** build the image inside DinD, push to `registry.homecredit.vn`.

**Simulate it** with a local registry + a one-off DinD daemon — no GitLab needed:

```bash
# 1) start a standalone registry (our 'registry.homecredit.vn' stand-in)
docker run -d --name lab-registry -p 5000:5000 registry:2

# 2) build the app image and push it (the script does both)
./simulation/scripts/stage2-build.sh v0.0.1
```

`stage2-build.sh` runs the same commands as the `build-app` job:

```bash
IMAGE="registry.local:5000/service_desk/sd-automation-hub:${1:-v0.0.1}"
docker build \
  --build-arg BUILD_VERSION="${1:-v0.0.1}" \
  -t "$IMAGE" .
docker push "$IMAGE"
```

**Verify** the image really landed in the registry:

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

# 2) make the built image available to the cluster (sideload — no registry pull needed)
kind load docker-image registry.local:5000/service_desk/sd-automation-hub:v0.0.1 --name sdah

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
# open http://localhost:8501 in a browser
```

### 5.4 Secrets (simulating Vault)

Production injects secrets from Vault (provisioned via `spiral-scheme`). Two
fidelity levels:

**Minimum (recommended for the lab) — a plain K8s Secret:**

```bash
# build a Secret from the example env file (dummy values are fine in the lab)
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

### 6.1 Start GitLab + runner + registry

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

### 6.2 Create the two projects

In the GitLab UI create:

1. `sd-automation-hub` — push **this** repo into it.
2. `sd-automation-hub-env` — the environments repo; add
   `sd-automation-hub/deployment.yml` on a branch named `sd-automation-hub-release`.

```bash
git remote add lab http://root@gitlab.local:8080/root/sd-automation-hub.git
git push lab claude/busy-heisenberg-m89mrp:main
```

### 6.3 Register the runner with DinD

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

### 6.4 Set CI/CD variables

In the `sd-automation-hub` project → **Settings → CI/CD → Variables**:

| Key | Value (lab) | Flags |
| --- | --- | --- |
| `REGISTRY_USER` | `lab` | masked |
| `REGISTRY_PASSWORD` | `lab` | masked |
| `GITLAB_PF_TOKEN` | a project token with `write_repository` on the env repo | masked, protected |

Also protect the tag pattern `v*` under **Settings → Repository → Protected tags**
so protected variables are available to tag pipelines.

### 6.5 Use the lab pipeline and run it

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
| `deploy` (commit) | env repo has a new commit bumping the tag | `git -C /tmp/env-repo log --oneline -1` |
| `deploy` (sync) | ArgoCD app `Synced` + `Healthy` | `kubectl get applications -n argocd` |
| runtime | pod `Running`, healthcheck `ok` | `kubectl get pods` + `curl .../_stcore/health` |

---

## 8. Troubleshooting

- **GitLab is slow / unhealthy on boot.** Give it 4 GB+ and ~5 minutes. Check
  `docker compose -f docker-compose.lab.yml logs gitlab`. The container is
  unhealthy until reconfigure finishes — that's normal.
- **Runner job: "Cannot connect to the Docker daemon".** The runner needs
  `--docker-privileged`; the build job needs matching `DOCKER_HOST` /
  `DOCKER_TLS_CERTDIR`. The lab pipeline disables TLS (`DOCKER_TLS_CERTDIR=""`,
  `DOCKER_HOST=tcp://docker:2375`) to keep it simple.
- **`docker push` → "http: server gave HTTP response to HTTPS client".** The
  local registry is plain HTTP. The lab DinD service starts with
  `--insecure-registry registry.local:5000`. For plain local `docker` (Track A),
  add `"insecure-registries": ["localhost:5000"]` to the daemon config and
  restart Docker.
- **kind pod stuck `ImagePullBackOff`.** Easiest fix: `kind load docker-image <img>`
  and set `imagePullPolicy: IfNotPresent` (already set in the sample manifest).
- **Job containers can't resolve `gitlab.local` / `registry.local`.** Register the
  runner with `--docker-network-mode sdah-lab_lab` (the compose network name).
- **ArgoCD won't sync.** Confirm `repoURL`, `targetRevision: sd-automation-hub-release`,
  and `path: sd-automation-hub` in the Application match your env repo.

---

## 9. Teardown

```bash
# Track A
docker rm -f lab-registry lab-vault 2>/dev/null
kind delete cluster --name sdah
rm -rf /tmp/env-repo

# Track B
cd simulation && docker compose -f docker-compose.lab.yml down -v
```

`-v` removes the GitLab/registry volumes too — omit it if you want to keep state
between sessions.

---

## 10. From lab to production

When the lab is green, here's exactly what changes for the real Home Credit run
(nothing structural — only endpoints, auth, and TLS):

| Lab | Production |
| --- | --- |
| `registry.local:5000`, no auth, HTTP | `registry.homecredit.vn`, **service account**, TLS |
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
> refactored.
