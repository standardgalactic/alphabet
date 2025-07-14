from PIL import Image

def embed_image(base_image_path, embed_image_path, output_path):
    base_image = Image.open(base_image_path)
    embed_image = Image.open(embed_image_path)

    base_pixels = list(base_image.getdata())
    embed_pixels = list(embed_image.getdata())

    new_pixels = []

    for base_pixel, embed_pixel in zip(base_pixels, embed_pixels):
        new_pixel = (
            (base_pixel[0] & ~1) | (embed_pixel[0] >> 7),
            (base_pixel[1] & ~1) | (embed_pixel[1] >> 7),
            (base_pixel[2] & ~1) | (embed_pixel[2] >> 7),
        )
        new_pixels.append(new_pixel)

    base_image.putdata(new_pixels)
    base_image.save(output_path)
    print(f"Image embedded and saved as {output_path}")

if __name__ == "__main__":
    base_image_path = "old-profile.png"
    embed_image_path = "raccoon-image.png"
    output_path = "steganographic-profile.png"

    embed_image(base_image_path, embed_image_path, output_path)
