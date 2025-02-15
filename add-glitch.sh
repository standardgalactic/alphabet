#!/bin/bash

# Original image path
original="original.png"

# Create frames with various glitch effects
for i in {1..20}; do
    # Work with a copy of the original for each frame
    cp "$original" "frame_$i.png"
    
    # Apply a central focus pixelation effect by masking the center
    convert "frame_$i.png" \( +clone -region 50x50% -scale 50% -scale 200% \) -gravity center -composite "frame_$i.png"
    
    # Apply a spread effect but only on the center
    convert "frame_$i.png" \( +clone -gravity center -crop 50x50% +repage -spread $((RANDOM % 5)) \) -gravity center -composite "frame_$i.png"

    # Simulate a subtle greenish flash effect by adjusting brightness/contrast
    if [ $((i % 2)) -eq 0 ]; then
        convert "frame_$i.png" -modulate 100,100,120 "frame_$i.png"
    fi
done

# Combine all frames into a single GIF
convert -delay 20 -loop 0 frame_*.png glitched_monitor.gif

# Clean up temporary frame files
rm frame_*.png

# Commenting out the email part as requested
#echo "Here is your glitched monitor simulation." | mutt -s "Glitched Monitor GIF" -a glitched_monitor.gif -- nateguimondaer@gmail.com
