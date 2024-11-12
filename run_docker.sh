#!/bin/bash

DOCKER_IMAGE_TAG="iamhexi/knowledge_verificator"
REBUILD=false

show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo
    echo "Options:"
    echo "  --rebuild    Force rebuild the Docker image from the Dockerfile."
    echo "  --help       Display this help message."
    echo
    echo "This script builds and runs a Docker container for the specified image."
}

for arg in "$@"; do
    case $arg in
        --help)
            show_help
            exit 0
            ;;
        --rebuild)
            REBUILD=true
            ;;
    esac
done

if $REBUILD || ! sudo docker image inspect "$DOCKER_IMAGE_TAG" > /dev/null 2>&1; then
    echo "Building Docker image $DOCKER_IMAGE_TAG..."
    sudo docker build -t "$DOCKER_IMAGE_TAG" .
else
    echo "Docker image $DOCKER_IMAGE_TAG already exists."
fi

echo "Running Docker container..."
sudo docker run --network=host "$DOCKER_IMAGE_TAG"
