#!/bin/bash

DOCKER_IMAGE_TAG="imahexi/knowledge_verificator"
REBUILD=false
USE_GPU=false

# Function to display help information
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo
    echo "Options:"
    echo "  --rebuild    Force rebuild the Docker image from the Dockerfile."
    echo "  --gpu        Use GPU support when running the Docker container."
    echo "  --help       Display this help message."
    echo
    echo "This script builds and runs a Docker container for the specified image."
    echo
    echo "Note: Using the --gpu option requires the NVIDIA Container Toolkit to be installed."
}

# Check for the --help, --rebuild, and --gpu arguments
for arg in "$@"; do
    case $arg in
        --help)
            show_help
            exit 0
            ;;
        --rebuild)
            REBUILD=true
            ;;
        --gpu)
            USE_GPU=true
            ;;
    esac
done

# Check if the Docker image exists
if $REBUILD || ! sudo docker image inspect "$DOCKER_IMAGE_TAG" > /dev/null 2>&1; then
    echo "Building Docker image $DOCKER_IMAGE_TAG..."
    sudo docker build --platform linux/amd64,linux/arm64 -t "$DOCKER_IMAGE_TAG" .
else
    echo "Docker image $DOCKER_IMAGE_TAG already exists."
fi

# Prepare the docker run command
DOCKER_RUN_CMD="sudo docker run --network=host"

# Add GPU support if --gpu is specified
if $USE_GPU; then
    # Check if NVIDIA Container Toolkit is installed
    if ! command -v nvidia-smi &> /dev/null; then
        echo "Error: NVIDIA Container Toolkit is not installed. Please install it to use GPU support."
        exit 1
    fi
    DOCKER_RUN_CMD+=" --gpus all"  # Use all available GPUs
fi

# Run the Docker container
echo "Running Docker container..."
$DOCKER_RUN_CMD "$DOCKER_IMAGE_TAG"
