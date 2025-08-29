#!/usr/bin/env bash
set -e

# ============================================================
# CONFIG
# ============================================================
ACR_NAME="dokcerregistery"   # 👈 change this to your ACR name (without .azurecr.io)
ACR_LOGIN_SERVER="${ACR_NAME}.azurecr.io"

# Default version if not passed
VERSION=${1:-v1}

# List of service folders
SERVICES=(
  csv-service
  excel-service
  image-service
  pdf-service
  pptx-service
  web-scraping-service
  word-service
)

# ============================================================
# LOGIN TO ACR
# ============================================================
echo "🔑 Logging in to ACR: $ACR_NAME ..."
az acr login --name "$ACR_NAME"

# ============================================================
# BUILD & PUSH
# ============================================================
for SERVICE in "${SERVICES[@]}"; do
  IMAGE="$ACR_LOGIN_SERVER/$SERVICE:$VERSION"

  echo "🐳 Building image for $SERVICE with tag $VERSION ..."
  docker build -t "$IMAGE" "./$SERVICE"

  echo "📤 Pushing $IMAGE ..."
  docker push "$IMAGE"

  echo "✅ $SERVICE pushed successfully!"
done

echo "🎉 All images built and pushed to $ACR_LOGIN_SERVER with tag: $VERSION"
