#!/bin/bash
# Build and publish Docker image

set -e

DOCKER_REPO=${DOCKER_REPO:-yourusername/smart-attendance}
VERSION=$(grep "version=" setup.py | head -n1 | grep -oP '\d+\.\d+\.\d+')

echo "🐳 Building Docker image..."
echo "Repository: $DOCKER_REPO"
echo "Version: $VERSION"
echo ""

# Build image
docker build -t $DOCKER_REPO:$VERSION -t $DOCKER_REPO:latest .

echo "✅ Build complete!"
echo ""

# Push to Docker Hub
if [ "$1" == "--push" ]; then
    echo "📤 Pushing to Docker Hub..."
    docker push $DOCKER_REPO:$VERSION
    docker push $DOCKER_REPO:latest
    echo "✅ Published!"
    echo ""
    echo "Users can now run:"
    echo "  docker run -it $DOCKER_REPO:latest"
    echo "  docker run -it $DOCKER_REPO:$VERSION"
else
    echo "ℹ️  To push to Docker Hub, run:"
    echo "  ./scripts/publish-docker.sh --push"
    echo ""
    echo "First, ensure you're logged in:"
    echo "  docker login"
fi
