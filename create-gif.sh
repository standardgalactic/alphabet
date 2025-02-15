#!/bin/bash

# Create a temporary directory for images
temp_dir=$(mktemp -d)
trap 'rm -rf "$temp_dir"' EXIT

# Generate base images
for i in {1..10}; do
    # Create a black image
    convert -size 320x240 xc:black "$temp_dir/frame_$i.png"
    
    # Add bright green text in even frames
    if [ $((i % 2)) -eq 0 ]; then
        # Create the text image separately
        convert -background none -fill "#00FF00" -font Arial -pointsize 36 label:"LIVE NOW" "$temp_dir/text_$i.png"
        
        # Composite the text onto the black background
        convert "$temp_dir/frame_$i.png" "$temp_dir/text_$i.png" -gravity Center -composite "$temp_dir/frame_$i.png"
    fi

    # Random glitch effect (distort the image)
    if [ $((RANDOM % 2)) -eq 0 ]; then
        convert "$temp_dir/frame_$i.png" -scale 110% -gravity Center -crop 100%x100% +repage "$temp_dir/frame_$i.png"
    fi
    
    # Add noise to simulate a monitor effect
    convert "$temp_dir/frame_$i.png" -noise 3 "$temp_dir/frame_$i.png"
    
    # Add scan lines
    convert "$temp_dir/frame_$i.png" \( +clone -threshold 50% -negate -virtual-pixel black -spread 2 \) -compose Overlay -composite "$temp_dir/frame_$i.png"

    # Crop the image to better fit the text
    convert "$temp_dir/frame_$i.png" -trim +repage -gravity Center -background black -extent 320x240 "$temp_dir/frame_$i.png"
done

# Create GIF from generated frames with reduced framerate for slower flashing
ffmpeg -y -framerate 5 -i "$temp_dir/frame_%d.png" -loop 0 live-now.gif

echo "GIF created: live-now.gif"
