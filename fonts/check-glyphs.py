import fontforge
import os

def probe_font(path):
    try:
        f = fontforge.open(path)
        print(f"== {path} ==")
        print("Fontname:", f.fontname)
        print("Family:", f.familyname)
        print("Fullname:", f.fullname)
        print("Encoding:", f.encoding)
        print("Glyph count:", len(list(f.glyphs())))
        # Print first 10 glyphs
        for i, g in enumerate(f.glyphs()):
            print(f"  {i}: {g.glyphname} (U+{g.unicode:04X})")
            if i >= 9: break
        print()
        f.close()
    except Exception as e:
        print(f"Error reading {path}: {e}")

for fname in os.listdir('.'):
    if fname.lower().endswith(('.ttf', '.otf')):
        probe_font(fname)
