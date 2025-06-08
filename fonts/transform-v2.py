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
    font.weight = "Regular"
    font.copyright = "Copyright 2025 Debug"
    font.version = "001.000"

def ensure_required_glyphs(src_font, dst_font):
    # Copy .notdef, .null, space if they exist
    for gname in (".notdef", ".null", "space"):
        if gname in src_font:
            src = src_font[gname]
            dst = dst_font.createChar(src.unicode, gname) if src.unicode != -1 else dst_font.createChar(-1, gname)
            dst.width = src.width
            dst.clear()
            dst.foreground = src.foreground
    # At minimum, you want .notdef and space for a valid font

def copy_glyph(src_glyph, dst_font):
    dst_glyph = dst_font.createChar(src_glyph.unicode, src_glyph.glyphname) if src_glyph.unicode != -1 else dst_font.createChar(-1, src_glyph.glyphname)
    dst_glyph.width = src_glyph.width
    dst_glyph.clear()
    dst_glyph.foreground = src_glyph.foreground
    for ref in src_glyph.references:
        dst_glyph.addReference(ref[0], ref[1])
    return dst_glyph

def main():
    src_font_path = "Systada-Regular.ttf"  # Change as needed
    out_ttf = "robust_ascii.ttf"
    out_png = "robust_ascii_preview.png"
    src_font = fontforge.open(src_font_path)
    new_font = fontforge.font()
    new_font.em = src_font.em
    set_font_metadata(new_font, "RobustASCII", "Robust ASCII", "Robust ASCII")

    # Set encoding to Unicode full to be safe
    new_font.encoding = "UnicodeFull"
    ensure_required_glyphs(src_font, new_font)

    for c in ASCII_ALL:
        code = ord(c)
        if code not in src_font:
            print(f"Missing {c}")
            continue
        g = src_font[code]
        new_glyph = copy_glyph(g, new_font)
        # You could make visual changes here

    # (Optional) Set OS/2 table values for compatibility
    new_font.os2_family_class = 0  # No family class
    new_font.os2_weight = 400
    new_font.os2_width = 5
    new_font.os2_fstype = 0

    # Generate and close
    new_font.generate(out_ttf)
    new_font.close()
    print("Generated", out_ttf)

    # Preview
    img = Image.new('RGB', (1000, 200), color='white')
    draw = ImageDraw.Draw(img)
    try:
        fnt = ImageFont.truetype(out_ttf, 64)
        draw.text((10, 40), "ABCDEFGHIJKLMNOPQRSTUVWXYZ\nabcdefghijklmnopqrstuvwxyz", font=fnt, fill='black')
    except Exception as e:
        draw.text((10, 40), f"Error: {e}", fill='red')
    img.save(out_png)
    print("Preview written to", out_png)

if __name__ == "__main__":
    main()
