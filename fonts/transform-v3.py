import fontforge
import os

# Define transformations
def italicize(glyph, degrees=12):
    angle = degrees * 3.14159 / 180.0
    glyph.transform((1, 0, angle, 1, 0, 0))

def embolden(glyph, strength=40):
    glyph.changeWeight(strength, "auto", 0, 0, "auto")

def outline(glyph, width=30):
    glyph.stroke("circular", width, "round", "round")
    glyph.removeOverlap()
    glyph.simplify()

def shadow(glyph, offset_x=60, offset_y=-40):
    orig = glyph.foreground.copy()
    glyph.foreground.translate(offset_x, offset_y)
    glyph.foreground += orig

def condense(glyph, factor=0.7):
    glyph.transform((factor, 0, 0, 1, 0, 0))

def expand(glyph, factor=1.3):
    glyph.transform((factor, 0, 0, 1, 0, 0))

# List of style transformations to apply
transformations = [
    ("italic", italicize),
    ("bold", embolden),
    ("outline", outline),
    ("shadow", shadow),
    ("condense", condense),
    ("expand", expand),
]

def process_font(path, out_dir="styled_fonts"):
    basename = os.path.splitext(os.path.basename(path))[0]
    for style_name, style_fn in transformations:
        font = fontforge.open(path)
        font.fontname = f"{basename}_{style_name}"
        font.familyname = f"{basename} {style_name.capitalize()}"
        font.fullname = f"{basename} {style_name.capitalize()}"
        for glyph in font.glyphs():
            try:
                style_fn(glyph)
            except Exception as e:
                print(f"Error transforming {glyph.glyphname} in {basename}: {e}")
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, f"{basename}_{style_name}.ttf")
        font.generate(out_path)
        font.close()
        print(f"Generated {out_path}")

def main():
    for fname in os.listdir('.'):
        if fname.lower().endswith(('.ttf', '.otf')):
            print(f"Processing {fname}")
            process_font(fname)

if __name__ == "__main__":
    main()
