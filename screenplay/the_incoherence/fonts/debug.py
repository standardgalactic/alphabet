import fontforge
import os
from PIL import Image, ImageDraw, ImageFont

ASCII_UPPER = [chr(c) for c in range(ord('A'), ord('Z')+1)]
ASCII_LOWER = [chr(c) for c in range(ord('a'), ord('z')+1)]
ASCII_ALL = ASCII_UPPER + ASCII_LOWER

def set_font_metadata(font, fontname, family, fullname):
    font.fontname = fontname
    font.familyname = family
    font.fullname = fullname
    font.copyright = "Debug FontForge Script"

def save_font(font, output_path):
    font.generate(output_path)
    font.close()
    print(f"Saved font to {output_path}")

def preview_chart(ttf_path, out_png="preview.png", text="ABCDEFGHIJKLMNOPQRSTUVWXYZ\nabcdefghijklmnopqrstuvwxyz"):
    img = Image.new('RGB', (1000, 200), color='white')
    draw = ImageDraw.Draw(img)
    try:
        fnt = ImageFont.truetype(ttf_path, 64)
        draw.text((10, 40), text, font=fnt, fill='black')
    except Exception as e:
        draw.text((10, 40), "FAILED TO LOAD FONT: " + str(e), fill='red')
    img.save(out_png)
    print(f"Saved preview to {out_png}")

def test_copy_ascii_glyphs(src_font_path, out_font_path, alteration="shift"):
    src_font = fontforge.open(src_font_path)
    new_font = fontforge.font()
    new_font.em = src_font.em
    set_font_metadata(new_font, "TestASCII", "Test ASCII", "Test ASCII")
    coverage = []
    for c in ASCII_ALL:
        try:
            code = ord(c)
            if code not in src_font:
                print(f"Source font does not have glyph for '{c}' ({code})")
                continue
            glyph = src_font[code]
            new_glyph = new_font.createChar(code, glyph.glyphname)
            new_glyph.width = glyph.width
            new_glyph.clear()
            new_glyph.foreground = glyph.foreground
            # VISUAL ALTERATION: shift right for upper, left for lower
            if alteration == "shift":
                dx = 100 if c.isupper() else -100
                new_glyph.transform((1, 0, 0, 1, dx, 0))
            elif alteration == "scale":
                scale = 1.5 if c.isupper() else 0.5
                new_glyph.transform((scale, 0, 0, scale, 0, 0))
            elif alteration == "box":
                pen = new_glyph.glyphPen()
                pen.moveTo((10, 10))
                pen.lineTo((10, 100))
                pen.lineTo((100, 100))
                pen.lineTo((100, 10))
                pen.closePath()
            coverage.append(c)
            print(f"Copied and altered '{c}' ({code})")
        except Exception as e:
            print(f"Error copying '{c}': {e}")
    save_font(new_font, out_font_path)
    print("Coverage:", ''.join(coverage))

def main():
    # Try different source fonts if needed
    src_fonts = [
        "Systada-Regular.ttf",
        "Cheiro-Regular.ttf",
        "Clypto-Regular.ttf"
    ]
    alteration_types = ["shift", "scale", "box"]
    output_dir = "ascii_debug_out"
    os.makedirs(output_dir, exist_ok=True)
    for font_path in src_fonts:
        if not os.path.exists(font_path):
            print(f"Font not found: {font_path}")
            continue
        for alteration in alteration_types:
            out_font = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(font_path))[0]}_{alteration}_ascii.ttf")
            out_png = out_font.replace(".ttf", ".png")
            print(f"\n==== {font_path} | {alteration} ====")
            test_copy_ascii_glyphs(font_path, out_font, alteration=alteration)
            preview_chart(out_font, out_png)
    print("\nDONE.")

if __name__ == "__main__":
    main()
