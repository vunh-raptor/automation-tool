#!/usr/bin/env bash
# Stage 3 (deploy): the GitOps tag bump that the production `deploy-app` job does.
# Rewrites the image tag in the env repo's manifest and commits it.
# Usage: stage3-deploy.sh <tag> <env-repo-dir>
set -euo pipefail

TAG="${1:?usage: stage3-deploy.sh <tag> <env-repo-dir>}"
ENV_REPO="${2:?usage: stage3-deploy.sh <tag> <env-repo-dir>}"
REGISTRY="${REGISTRY:-registry.local:5000}"
IMAGE_PATH="service_desk/sd-automation-hub"
MANIFEST="${ENV_REPO}/sd-automation-hub/deployment.yml"

[ -f "${MANIFEST}" ] || { echo "manifest not found: ${MANIFEST}" >&2; exit 1; }

# GNU sed (Linux). On macOS use: sed -i '' ...
sed -i "s|image: ${REGISTRY}/${IMAGE_PATH}:.*|image: ${REGISTRY}/${IMAGE_PATH}:${TAG}|" "${MANIFEST}"

git -C "${ENV_REPO}" add sd-automation-hub/deployment.yml
if git -C "${ENV_REPO}" diff --cached --quiet; then
  echo "deploy: no change (manifest already at ${TAG})"
else
  git -C "${ENV_REPO}" commit -m "Deploy sd-automation-hub:${TAG}"
  git -C "${ENV_REPO}" push origin sd-automation-hub-release 2>/dev/null \
    || echo "deploy: committed locally (no 'origin' remote configured yet)"
fi

echo "deploy: manifest image set to ${REGISTRY}/${IMAGE_PATH}:${TAG}"
echo "ArgoCD (if running) will now sync; otherwise: kubectl apply -f ${MANIFEST}"
