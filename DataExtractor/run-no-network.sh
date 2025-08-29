#!/usr/bin/env bash
set -e

###############################################################################
# 1. Define service folders and their corresponding ports
###############################################################################
declare -A SERVICE_PORTS=(
  [csv-service]=8021
  [excel-service]=8022
  [image-service]=8023
  [pdf-service]=8024
  [pptx-service]=8025
  [web-scraping-service]=8026
  [word-service]=8027
)

###############################################################################
# 2. Loop through each service: build and run
###############################################################################
for SERVICE in "${!SERVICE_PORTS[@]}"; do
  PORT="${SERVICE_PORTS[$SERVICE]}"
  IMAGE_NAME="${SERVICE}-image"
  CONTAINER_NAME="${SERVICE}"

  echo ""
  echo "📦 Entering ./$SERVICE"
  
  # Check directory and Dockerfile existence
  if [[ ! -d "./$SERVICE" || ! -f "./$SERVICE/Dockerfile" ]]; then
    echo "❌ Missing folder or Dockerfile in $SERVICE"
    exit 1
  fi

  # Move into the service directory
  cd "./$SERVICE" || {
    echo "❌ Failed to cd into $SERVICE"
    exit 1
  }

  echo "🔨 Building $IMAGE_NAME..."
  docker build -t "$IMAGE_NAME" . || {
    echo "❌ Build failed for $SERVICE"
    cd ..
    exit 1
  }

  cd ..

  echo "🛑 Stopping any existing container named $CONTAINER_NAME..."
  docker rm -f "$CONTAINER_NAME" 2>/dev/null || true

  echo "🚀 Running $SERVICE on port $PORT..."
  docker run -d \
    --name "$CONTAINER_NAME" \
    -p "$PORT:$PORT" \
    "$IMAGE_NAME"
done

echo ""
echo "✅ All services are built and running."
