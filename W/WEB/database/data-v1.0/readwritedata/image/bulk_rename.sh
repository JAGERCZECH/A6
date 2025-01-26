#!/bin/bash

# Directory containing the files
directory="/home/userland/A6/W/WEB/database/maindatabase/image/other/test"

# New filename prefix
new_prefix="image"

# Initialize a counter
counter=1

# Loop through each file in the directory
for file in "$directory"/*; do
  # Get the file extension
  extension="${file##*.}"
  
  # Define the new name for the file with the counter and extension
  newname="${new_prefix}${counter}.${extension}"
  
  # Rename the file
  mv "$file" "$directory/$newname"
  
  # Increment the counter
  counter=$((counter + 1))
done
