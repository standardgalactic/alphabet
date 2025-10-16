from PIL import Image, ImageFilter, ImageEnhance
import numpy as np

# --- parameters ---
width, height = 1654, 2339   # roughly A4 at 150 dpi
base_color = np.array([240, 224, 200], dtype=np.float32)  # light tan base
noise_layers = 5             # number of blended noise scales
seed = 42                    # for reproducibility
np.random.seed(seed)

# --- generate fractal noise ---
canvas = np.zeros((height, width), dtype=np.float32)
for i in range(noise_layers):
    scale = 2 ** i
    h_small, w_small = max(1, height // scale), max(1, width // scale)
    noise = np.random.rand(h_small, w_small)
    noise = np.kron(noise, np.ones((scale, scale)))
    
    # Pad or crop to match exact canvas size
    noise = noise[:height, :width]
    if noise.shape[0] < height:
        pad_h = height - noise.shape[0]
        noise = np.pad(noise, ((0, pad_h), (0, 0)), mode="edge")
    if noise.shape[1] < width:
        pad_w = width - noise.shape[1]
        noise = np.pad(noise, ((0, 0), (0, pad_w)), mode="edge")
    
    canvas += noise / (i + 1)

canvas /= canvas.max()

# --- apply gentle radial vignette ---
y, x = np.ogrid[:height, :width]
cy, cx = height / 2, width / 2
r = np.sqrt((x - cx)**2 + (y - cy)**2)
r /= r.max()
vignette = 1 - 0.4 * r**1.5
canvas *= vignette

# --- convert to RGB parchment ---
texture = np.clip(base_color * (0.8 + 0.4 * canvas[..., None]), 0, 255).astype(np.uint8)
img = Image.fromarray(texture, "RGB")

# --- optional enhancements ---
img = img.filter(ImageFilter.GaussianBlur(1.2))
img = ImageEnhance.Contrast(img).enhance(1.15)
img = ImageEnhance.Color(img).enhance(1.05)

# --- save ---
img.save("parchment.jpg", quality=95)
print("✅ Saved parchment.jpg successfully")
