for dir in Haplopraxis abraxas arcanum backward-compatibility calculator ensign library quadrivium sitemap standardgalactic.github.io; do
  echo "Processing $dir..."
  cd "$dir" || { echo "Failed to enter $dir"; continue; }

  # Ensure the fonts directory exists
  mkdir -p fonts

  # Copy new fonts
  cp -r ../alphabet/fonts/* fonts/
  echo "Copied new fonts to $dir/fonts/"

  # Commit and push changes
  git add fonts/
  git commit -m "Terminal Friendly Font"
  git push

  cd ..
  echo "Done with $dir, moving to next."
done

