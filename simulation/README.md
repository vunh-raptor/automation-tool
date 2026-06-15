# Local CI/CD Simulation Lab

Reproduce the production `verify → build → deploy` pipeline on your machine so you
can test and **verify each stage** before running it on Home Credit infrastructure.

**Full step-by-step guide:** [`../docs/local-ci-cd-simulation.md`](../docs/local-ci-cd-simulation.md)

## Contents

| File | Purpose |
| --- | --- |
| `docker-compose.lab.yml` | Self-hosted GitLab + runner + registry (Track B) |
| `.gitlab-ci.lab.yml` | Lab variant of the pipeline (local registry, DinD TLS off) |
| `kind/kind-cluster.yaml` | Local Kubernetes cluster config |
| `argocd/application.yaml` | ArgoCD Application pointing at the env repo |
| `k8s/deployment.yml` | Sample Deployment + Service for the env repo |
| `scripts/stage1-verify.sh` | Run the `verify` stage locally |
| `scripts/stage2-build.sh` | Build + push the image (the `build` stage) |
| `scripts/stage3-deploy.sh` | GitOps tag bump (the `deploy` stage) |

## One-time host setup

Add to `/etc/hosts` so the same registry/GitLab name works on the host **and**
inside the Docker network:

```
127.0.0.1 gitlab.local registry.local
```

Mark the lab registry insecure (it's plain HTTP) in `/etc/docker/daemon.json`,
then restart Docker:

```json
{ "insecure-registries": ["registry.local:5000"] }
```

## Quick start (Track A — no GitLab needed)

```bash
./scripts/stage1-verify.sh                       # stage: verify
docker run -d --name lab-registry -p 5000:5000 registry:2
./scripts/stage2-build.sh v0.0.1                 # stage: build
# then create a kind cluster + ArgoCD and run stage3-deploy.sh — see the guide
```
