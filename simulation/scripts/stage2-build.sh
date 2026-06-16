#!/usr/bin/env bash
# Stage 2 (build): build the app image and push it to the local registry.
# Run it INSIDE your WSL2 distro. Mirrors the production `build-app` job
# (minus the corporate proxy/TLS, which only apply inside the HC network).
#
# Usage: ./stage2-build.sh [tag]      (default tag: v0.0.1)
#
# Default registry is localhost:5000 — Docker treats it as insecure
# automatically, so there is NO Docker Desktop config to edit.
# For the Track B in-network registry: REGISTRY=registry.local:5000 ./stage2-build.sh
set -euo pipefail

cd "$(dirname "$0")/../.."

TAG="${1:-v0.0.1}"
REGISTRY="${REGISTRY:-localhost:5000}"
IMAGE="${REGISTRY}/service_desk/sd-automation-hub:${TAG}"

echo "Building ${IMAGE} ..."
docker build --build-arg BUILD_VERSION="${TAG}" -t "${IMAGE}" .
docker push "${IMAGE}"

echo "build: pushed ${IMAGE}"
echo "verify with: curl -s http://${REGISTRY}/v2/_catalog"
