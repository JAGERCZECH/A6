#!/bin/bash

# Get the number of Nginx containers to launch from user input
NUM_CONTAINERS=$1

# Check if number of containers is provided, else prompt for input
if [ -z "$NUM_CONTAINERS" ]; then
  read -p "Enter the number of Nginx containers to launch: " NUM_CONTAINERS
fi

# Check if NUM_CONTAINERS is a valid number
if ! [[ "$NUM_CONTAINERS" =~ ^[0-9]+$ ]]; then
  echo "Error: The input is not a valid number."
  exit 1
fi

# Launch Docker Nginx containers
for ((i=0; i<$NUM_CONTAINERS; i++)); do
  # Prompt user for port number
  read -p "Enter the port number to map for container $((i + 1)): " PORT

  # Check if PORT is a valid number
  if ! [[ "$PORT" =~ ^[0-9]+$ ]]; then
    echo "Error: The port number is not valid."
    exit 1
  fi

  # Launch the Nginx container and map the given port
  echo "Launching Nginx container $((i + 1)) on port $PORT"
  docker run -d -p $PORT:80 nginx
done

echo "Launched $NUM_CONTAINERS Nginx containers."
