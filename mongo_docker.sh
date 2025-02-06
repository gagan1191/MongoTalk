#!/bin/bash

# Set MongoDB container name
CONTAINER_NAME="mongo_docker"

# Check if MongoDB container is already running
if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
    echo "✅ MongoDB container '$CONTAINER_NAME' is already running."
else
    echo "🚀 Starting MongoDB container..."
    docker run -d \
        --name $CONTAINER_NAME \
        -p 27017:27017 \
        mongo:latest
    echo "✅ MongoDB container started successfully."
fi

# Wait for MongoDB to be ready
echo "⏳ Waiting for MongoDB to start..."
sleep 5  # Give it time to initialize

echo "🎯 MongoDB is running on mongodb://localhost:27017"
