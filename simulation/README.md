# Local CI/CD Simulation Lab (Windows 11 Home + WSL2 + Docker Desktop)

Reproduce the production `verify → build → deploy` pipeline on a Windows 11 Home
laptop so you can test and **verify each stage** before running it on Home Credit
infrastructure. Your **WSL2 + Docker Desktop (WSL2 backend)** setup is all that's
needed — no Windows Pro, no Hyper‑V Manager, no separate Linux VM.

**Full step-by-step guide:** [`../docs/local-ci-cd-simulation.md`](../docs/local-ci-cd-simulation.md)

> Run the `*.sh` scripts **inside your WSL2 distro** (Ubuntu), not PowerShell.
> The one `.ps1` helper is the exception — it runs in an elevated Windows
> PowerShell.

## Contents

| File | Purpose | Where it runs |
| --- | --- | --- |
| `docker-compose.lab.yml` | Self-hosted GitLab + runner + registry (Track B) | WSL2 |
| `.gitlab-ci.lab.yml` | Lab variant of the pipeline (local registry, DinD TLS off) | GitLab runner |
| `kind/kind-cluster.yaml` | Local Kubernetes cluster config (maps app to `localhost:8501`) | WSL2 |
| `argocd/application.yaml` | ArgoCD Application pointing at the env repo | cluster |
| `k8s/deployment.yml` | Sample Deployment + Service for the env repo | cluster |
| `scripts/stage1-verify.sh` | Run the `verify` stage locally | WSL2 |
| `scripts/stage2-build.sh` | Build + push the image (the `build` stage) | WSL2 |
| `scripts/stage3-deploy.sh` | GitOps tag bump (the `deploy` stage) | WSL2 |
| `scripts/win-hosts-setup.ps1` | (Track B) add `gitlab.local`/`registry.local` to the Windows hosts file | elevated PowerShell |
| `wsl/.wslconfig.example` | (Track B) give WSL2 enough RAM for GitLab | copy to `C:\Users\<you>\.wslconfig` |

## Quick start (Track A — no GitLab needed)

Inside WSL2, from the repo root:

```bash
./simulation/scripts/stage1-verify.sh                  # stage: verify
docker run -d --name lab-registry -p 5000:5000 registry:2
./simulation/scripts/stage2-build.sh v0.0.1            # stage: build
# then create a kind cluster + ArgoCD and run stage3-deploy.sh — see the guide
```

`localhost:5000` is treated as insecure by Docker automatically, so Track A needs
**no** Docker Engine config. Only Track B's `registry.local:5000` needs the
insecure-registries setting (see the guide, §6.1).
