from PIL import Image

def decode_image(encoded_image_path, output_path):
    encoded_image = Image.open(encoded_image_path)
    encoded_pixels = list(encoded_image.getdata())

    extracted_pixels = []

    for pixel in encoded_pixels:
        extracted_pixel = (
            (pixel[0] & 1) * 255,
            (pixel[1] & 1) * 255,
            (pixel[2] & 1) * 255,
        )
        extracted_pixels.append(extracted_pixel)

    extracted_image = Image.new(encoded_image.mode, encoded_image.size)
    extracted_image.putdata(extracted_pixels)
    extracted_image.save(output_path)
    print(f"Extracted image saved as {output_path}")

if __name__ == "__main__":
    encoded_image_path = "steganographic-profile.png"
    output_path = "extracted-raccoon.png"

    decode_image(encoded_image_path, output_path)
