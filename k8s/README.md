# Deploying SD Automation Hub on Kubernetes

This directory contains the manifests needed to run the SD Automation Hub
(Streamlit + Selenium) on a Kubernetes cluster.

## Files

| File              | Purpose                                                        |
|-------------------|----------------------------------------------------------------|
| `namespace.yaml`  | Dedicated `automation-hub` namespace                           |
| `configmap.yaml`  | Chromium/Selenium + Streamlit runtime settings                 |
| `deployment.yaml` | Pod spec (non-root, probes, resources, `/dev/shm` for Chrome)  |
| `service.yaml`    | ClusterIP service exposing port 80 → container 8501            |
| `ingress.yaml`    | NGINX ingress with WebSocket + sticky-session settings         |
| `kustomization.yaml` | Bundles everything for `kubectl apply -k`                   |

## 1. Build and push the image

```bash
docker build -t ghcr.io/vunh-raptor/automation-tool:latest .
docker push ghcr.io/vunh-raptor/automation-tool:latest
```

## 2. Set the image (optional)

Edit the tag in `kustomization.yaml`, or run:

```bash
cd k8s
kustomize edit set image ghcr.io/vunh-raptor/automation-tool=<registry>/<image>:<tag>
```

## 3. Update the ingress host

Change `automation-hub.example.com` in `ingress.yaml` to your own DNS name,
and (optionally) enable the TLS block.

## 4. Apply

```bash
kubectl apply -k k8s/
```

## 5. Verify

```bash
kubectl -n automation-hub get pods,svc,ingress
kubectl -n automation-hub logs deploy/sd-automation-hub -f

# Quick local access without an ingress:
kubectl -n automation-hub port-forward deploy/sd-automation-hub 8501:8501
# then open http://localhost:8501
```

## Notes

- **Single replica / sticky sessions:** Streamlit holds session state in the
  pod's memory, so the ingress is configured with cookie affinity. If you scale
  beyond one replica, keep the affinity annotations.
- **Chromium needs shared memory:** the deployment mounts a 1Gi in-memory
  `/dev/shm` to stop Chrome from crashing under load.
- **Windows-only features:** the *Send Email* page uses `win32com` (Outlook) and
  will not work in a Linux container. All other pages are unaffected.
- **Internal endpoints:** automation targets (HOSEL SSO, JIRA, internal sites)
  must be reachable from the cluster's network for those features to function.
