for dir in Haplopraxis abraxas arcanum calculator ensign library quadrivium sitemap standardgalactic.github.io; do
  if [ -d "$dir/fonts" ]; then
    cp -r alphabet/fonts/* "$dir/fonts/"
    echo "Copied to $dir/fonts/"
  else
    echo "Skipping $dir: fonts/ directory does not exist."
  fi
done

