#!/usr/bin/bash

output_file="overview.txt"

# Summarize all txt files

for file in {*.vtt,*.txt}; do
    if [ "$file" == "$output_file" ]; then
        echo "Skipping output file: $file" >> "$output_file"
        continue # Skip the summaries file itself
    fi

    if [ ! -s "$file" ]; then
        echo "Skipping empty file: $file" >> "$output_file"
        continue # Skip summarizing if the file is empty
    fi

    echo "Checking $file" | tee -a "$output_file"
    echo "=== Summary for $file ===" | tee -a "$output_file"
    ollama run vanilj/phi-4 "Translate the followingto Nigerian Pijin English, with no additional commentary or boilerplate: " < "$file" | tee -a "$output_file"
    echo -e "\n" | tee -a "$output_file" # Add a blank line between summaries
done
 
