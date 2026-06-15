#!/usr/bin/env bash
# Stage 2 (build): build the app image and push it to the local registry.
# Mirrors the production `build-app` job (minus proxy/TLS, which are prod-only).
# Usage: stage2-build.sh [tag]   (default tag: v0.0.1)
set -euo pipefail

cd "$(dirname "$0")/../.."

TAG="${1:-v0.0.1}"
REGISTRY="${REGISTRY:-registry.local:5000}"
IMAGE="${REGISTRY}/service_desk/sd-automation-hub:${TAG}"

echo "Building ${IMAGE} ..."
docker build --build-arg BUILD_VERSION="${TAG}" -t "${IMAGE}" .
docker push "${IMAGE}"

echo "build: pushed ${IMAGE}"
echo "verify with: curl -s http://localhost:5000/v2/_catalog"
