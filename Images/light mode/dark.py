import cv2
import numpy as np
import os

def process_image(file_path, background_hex):
# Convert hex color to BGR
  background_color = np.array([int(background_hex[i:i+2], 16) for i in (4, 2, 0)])

# Read the image
img = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)

# Check if image is in RGBA format (has an alpha
# channel)
  if img.shape[2] == 4:
# Separate the color and alpha
# channels
  color_layer, alpha_layer = img[:, :, :3], img[:, :, 3]

# Invert the color
# layer
inverted_color_layer = cv2.bitwise_not(color_layer)

# Create
# a new
# image
# with
# the
# inverted
# color
# layer
# and
# original
# alpha
# layer
new_img = np.dstack((inverted_color_layer, alpha_layer))

# Change
# the
# background
# color
# for
# transparent
# pixels
  mask = alpha_layer == 0
  new_img[mask] = background_color
  else:
# For
# images
# without
# alpha
# channel,
# just
# invert
# the
# colors
new_img = cv2.bitwise_not(img)

  return new_img

  def process_directory(directory, background_hex):
    for filename in os.listdir(directory):
      if filename.endswith(".png"):
  file_path = os.path.join(directory, filename)
      new_img = process_image(file_path, background_hex)
  new_file_path = os.path.join(directory, "processed_" + filename)
      cv2.imwrite(new_file_path, new_img)
      print(f"Processed {filename}")

# Use the current directory as the path
      directory_path = os.getcwd()
  background_hex = "0D1019"  # Background color in hex format

process_directory(directory_path, background_hex)

