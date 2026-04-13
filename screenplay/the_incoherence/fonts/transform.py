import fontforge
import os
from PIL import Image, ImageDraw, ImageFont

def set_font_metadata(font, fontname, family, fullname):
    font.fontname = fontname
    font.familyname = family
    font.fullname = fullname
    font.copyright = "Copyright 2025 Your Name"

def save_font(font, output_path, variant_name):
    """Save the modified font and generate a preview image."""
    try:
        font.generate(output_path)
        font.close()
        print(f"Saved {variant_name} font to {output_path}")
        # Generate a preview image using Pillow
        try:
            preview = Image.new('RGB', (800, 200), color='white')
            draw = ImageDraw.Draw(preview)
            pillow_font = ImageFont.truetype(output_path, 48)
            draw.text((10, 80), "Sample: ABCDEFabcdef123", font=pillow_font, fill='black')
            preview.save(output_path.replace('.ttf', '_preview.png'))
            print(f"Generated preview for {variant_name}")
        except Exception as e:
            print(f"Failed to generate preview for {variant_name}: {e}")
    except Exception as e:
        print(f"Failed to save {variant_name} font: {e}")

def copy_glyph(src_glyph, dst_font):
    """Copy outlines and properties from src_glyph into dst_font, return the new glyph."""
    if src_glyph.unicode != -1:
        dst_glyph = dst_font.createChar(src_glyph.unicode, src_glyph.glyphname)
    else:
        dst_glyph = dst_font.createChar(-1, src_glyph.glyphname)
    dst_glyph.width = src_glyph.width
    # Copy contours by merging foreground layers
    dst_glyph.foreground.clear()
    dst_glyph.foreground.append(src_glyph.foreground)
    # Copy glyph references (for composites)
    for ref in src_glyph.references:
        dst_glyph.addReference(ref[0], ref[1])
    return dst_glyph

def create_serif(font, output_path):
    """Add serifs to the font by extending stroke ends (illustrative: just copies glyphs)."""
    new_font = fontforge.font()
    new_font.em = font.em
    set_font_metadata(new_font, "MyFontSerif", "MyFont Serif", "MyFont Serif")
    for glyph in font.glyphs():
        if glyph.isWorthOutputting():
            try:
                new_glyph = copy_glyph(glyph, new_font)
                # Illustrative: you could add real serif logic here by editing new_glyph.foreground
            except Exception as e:
                print(f"Error processing glyph {glyph.glyphname}: {e}")
    save_font(new_font, output_path, "Serif")

def create_bubble(font, output_path):
    """Create a bubble version by inflating glyphs."""
    new_font = fontforge.font()
    new_font.em = font.em
    set_font_metadata(new_font, "MyFontBubble", "MyFont Bubble", "MyFont Bubble")
    for glyph in font.glyphs():
        if glyph.isWorthOutputting():
            try:
                new_glyph = copy_glyph(glyph, new_font)
                new_glyph.stroke("circular", 20, "round")
                new_glyph.simplify()
            except Exception as e:
                print(f"Error processing glyph {glyph.glyphname}: {e}")
    save_font(new_font, output_path, "Bubble")

def create_sans_serif(font, output_path):
    """Create a sans-serif version by simplifying strokes."""
    new_font = fontforge.font()
    new_font.em = font.em
    set_font_metadata(new_font, "MyFontSans", "MyFont Sans Serif", "MyFont Sans Serif")
    for glyph in font.glyphs():
        if glyph.isWorthOutputting():
            try:
                new_glyph = copy_glyph(glyph, new_font)
                new_glyph.simplify()
                new_glyph.round()
            except Exception as e:
                print(f"Error processing glyph {glyph.glyphname}: {e}")
    save_font(new_font, output_path, "Sans-Serif")

def create_nova_mono(font, output_path):
    """Create a monospaced Nova Mono-inspired version."""
    new_font = fontforge.font()
    new_font.em = font.em
    set_font_metadata(new_font, "MyFontNovaMono", "MyFont Nova Mono", "MyFont Nova Mono")
    fixed_width = 600
    for glyph in font.glyphs():
        if glyph.isWorthOutputting():
            try:
                new_glyph = copy_glyph(glyph, new_font)
                new_glyph.simplify()
                new_glyph.round()
                new_glyph.width = fixed_width
            except Exception as e:
                print(f"Error processing glyph {glyph.glyphname}: {e}")
    save_font(new_font, output_path, "Nova Mono")

def create_swash(font, output_path):
    """Add decorative swash flourishes to glyphs."""
    new_font = fontforge.font()
    new_font.em = font.em
    set_font_metadata(new_font, "MyFontSwash", "MyFont Swash", "MyFont Swash")
    for glyph in font.glyphs():
        if glyph.isWorthOutputting():
            try:
                new_glyph = copy_glyph(glyph, new_font)
                # Illustrative: add a simple swash curve to the right
                pen = new_glyph.glyphPen()
                width = new_glyph.width
                height = int(new_font.em * 0.5)
                pen.moveTo((width-20, height))
                pen.curveTo((width+50, height-50), (width+100, height-50), (width+150, height))
                pen.endPath()
            except Exception as e:
                print(f"Error processing glyph {glyph.glyphname}: {e}")
    save_font(new_font, output_path, "Swash")

def main():
    input_font_path = "Systada-Regular.ttf"  # Or try another .ttf from your directory!
    output_dir = "alterations"
    os.makedirs(output_dir, exist_ok=True)

    try:
        font = fontforge.open(input_font_path)
        create_serif(font, os.path.join(output_dir, "serif_font.ttf"))
        create_bubble(font, os.path.join(output_dir, "bubble_font.ttf"))
        create_sans_serif(font, os.path.join(output_dir, "sans_serif_font.ttf"))
        create_nova_mono(font, os.path.join(output_dir, "nova_mono_font.ttf"))
        create_swash(font, os.path.join(output_dir, "swash_font.ttf"))
        font.close()
    except Exception as e:
        print(f"Error processing font: {e}")

if __name__ == "__main__":
    main()
