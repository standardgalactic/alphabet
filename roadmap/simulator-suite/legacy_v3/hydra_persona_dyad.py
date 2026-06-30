import bpy
import math

# Clear
for obj in list(bpy.context.scene.objects):
    if obj.type in {"MESH", "CURVE"}:
        bpy.data.objects.remove(obj, do_unlink=True)

# Two personas: Seer & Engineer
personas = [
    ("Seer", (0.4, 0.8, 1.0, 1.0), (-3.0, 0.0, 0.0)),
    ("Engineer", (0.4, 1.0, 0.4, 1.0), (3.0, 0.0, 0.0)),
]

glyphs = []
for name, color, loc in personas:
    bpy.ops.mesh.primitive_circle_add(radius=1.0, vertices=8, location=loc)
    glyph = bpy.context.active_object
    glyph.name = f"Dyad_{name}_Glyph"
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0,0,0.3)})
    bpy.ops.object.editmode_toggle()
    mat = bpy.data.materials.new(f"Mat_Dyad_{name}")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Emission"].default_value = color
    bsdf.inputs["Emission Strength"].default_value = 4.0
    glyph.data.materials.append(mat)
    glyphs.append(glyph)

# Interaction bond ribbon
curve_data = bpy.data.curves.new("Dyad_Bond", 'CURVE')
curve_data.dimensions = '3D'
spline = curve_data.splines.new('BEZIER')
spline.bezier_points.add(2)
p0 = spline.bezier_points[0]
p1 = spline.bezier_points[1]
p2 = spline.bezier_points[2]

p0.co = (-3.0, 0.0, 0.5)
p1.co = (0.0, 0.0, 2.5)
p2.co = (3.0, 0.0, 0.5)

for p in spline.bezier_points:
    p.handle_left_type = p.handle_right_type = 'AUTO'

curve_data.bevel_depth = 0.12
bond = bpy.data.objects.new("Dyad_Bond", curve_data)
bpy.context.scene.collection.objects.link(bond)

bm = bpy.data.materials.new("Mat_Dyad_Bond")
bm.use_nodes = True
bsdf = bm.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Emission"].default_value = (0.8, 0.8, 1.0, 1.0)
bsdf.inputs["Emission Strength"].default_value = 5.0
curve_data.materials.append(bm)

# Shared entropic cloud
for i in range(40):
    import random
    x = random.uniform(-1.5,1.5)
    y = random.uniform(-0.4,0.4)
    z = random.uniform(0.5,1.8)
    bpy.ops.mesh.primitive_ico_sphere_add(radius=0.15, location=(x,y,z))
    s = bpy.context.active_object
    s.name = f"Dyad_Entropy_{i}"
    sm = bpy.data.materials.new(f"Mat_Dyad_Entropy_{i}")
    sm.use_nodes = True
    ebsdf = sm.node_tree.nodes["Principled BSDF"]
    ebsdf.inputs["Emission"].default_value = (1.0, 0.4, 0.7, 1.0)
    ebsdf.inputs["Emission Strength"].default_value = 6.0
    s.data.materials.append(sm)

print("[v3.3] HYDRA persona dyad created.")
