#!/bin/bash

# Function to list all running Docker containers
list_containers() {
  echo "Listing all running Docker containers:"
  docker ps
  echo
}

# Function to view logs of a specific container
view_logs() {
  read -p "Enter the container ID or name to view logs: " CONTAINER_ID
  echo "Showing logs for container $CONTAINER_ID:"
  docker logs "$CONTAINER_ID"
  echo
}

# Function to inspect a specific container
inspect_container() {
  read -p "Enter the container ID or name to inspect: " CONTAINER_ID
  echo "Inspecting container $CONTAINER_ID:"
  docker inspect "$CONTAINER_ID"
  echo
}

# Function to show top processes in a specific container
top_processes() {
  read -p "Enter the container ID or name to show top processes: " CONTAINER_ID
  echo "Showing top processes for container $CONTAINER_ID:"
  docker top "$CONTAINER_ID"
  echo
}

# Function to show stats for all running containers
show_stats() {
  echo "Showing stats for all running containers:"
  docker stats --no-stream
  echo
}

# Function to show Docker system disk usage
system_disk_usage() {
  echo "Showing Docker system disk usage:"
  docker system df
  echo
}

# Function to inspect a Docker network
inspect_network() {
  read -p "Enter the Docker network name to inspect: " NETWORK_NAME
  echo "Inspecting network $NETWORK_NAME:"
  docker network inspect "$NETWORK_NAME"
  echo
}

# Menu prompt
PS3="Please select an option: "
options=("List Containers" "View Logs" "Inspect Container" "Top Processes" "Show Stats" "System Disk Usage" "Inspect Network" "Quit")
select opt in "${options[@]}"; do
  case $opt in
    "List Containers")
      list_containers
      ;;
    "View Logs")
      view_logs
      ;;
    "Inspect Container")
      inspect_container
      ;;
    "Top Processes")
      top_processes
      ;;
    "Show Stats")
      show_stats
      ;;
    "System Disk Usage")
      system_disk_usage
      ;;
    "Inspect Network")
      inspect_network
      ;;
    "Quit")
      break
      ;;
    *)
      echo "Invalid option $REPLY"
      ;;
  esac
done
