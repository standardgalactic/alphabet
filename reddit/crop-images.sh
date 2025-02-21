#!/bin/bash

# Loop through all PNG files
for img in screencapture-*.png; do
# Get image height using vips
height=$(vipsheader -f height "$img")
width=$(vipsheader -f width "$img")

# Define crop height
crop_height=2000
num_pages=$(( (height + crop_height - 1) / crop_height ))  # Calculate required pages

# Loop through height, cropping in
# chunks
  for ((i=0; i<num_pages; i++)); do
y_offset=$((i * crop_height))
  output_file="${img%.png}_part${i}.png"

# Crop
# using
# vips
  vips crop "$img" "$output_file" 0 "$y_offset" "$width" "$crop_height"
  done
  done

  echo "Cropping complete!"

