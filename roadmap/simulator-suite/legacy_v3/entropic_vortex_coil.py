import bpy
import math

# Clear
for obj in list(bpy.context.scene.objects):
    if obj.type in {'MESH', 'CURVE'}:
        bpy.data.objects.remove(obj, do_unlink=True)

# Helical ribbons around z-axis
turns = 3
num_ribbons = 4
height = 8.0
radius = 3.0

for j in range(num_ribbons):
    curve_data = bpy.data.curves.new(f"VortexRibbon_{j}", 'CURVE')
    curve_data.dimensions = '3D'
    spline = curve_data.splines.new('POLY')
    steps = 64
    spline.points.add(steps-1)
    phase = (2*math.pi*j)/num_ribbons
    for i in range(steps):
        t = i / (steps-1)
        angle = 2*math.pi*turns*t + phase
        r = radius + 0.3*math.sin(4*angle)
        x = r*math.cos(angle)
        y = r*math.sin(angle)
        z = height*(t-0.5)
        spline.points[i].co = (x,y,z,1.0)
    curve_data.bevel_depth = 0.12
    obj = bpy.data.objects.new(f"VortexRibbon_{j}", curve_data)
    bpy.context.scene.collection.objects.link(obj)
    m = bpy.data.materials.new(f"Mat_VortexRibbon_{j}")
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    col = (0.4+0.15*j, 0.6, 1.0-0.1*j,1.0)
    bsdf.inputs["Emission"].default_value = col
    bsdf.inputs["Emission Strength"].default_value = 5.0
    curve_data.materials.append(m)

# center core
bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=height+1.0, location=(0,0,0))
core = bpy.context.active_object
core.name = "Vortex_Core"
cm = bpy.data.materials.new("Mat_VortexCore")
cm.use_nodes = True
cbsdf = cm.node_tree.nodes["Principled BSDF"]
cbsdf.inputs["Emission"].default_value = (0.9,0.9,1.0,1.0)
cbsdf.inputs["Emission Strength"].default_value = 4.0
core.data.materials.append(cm)

print("[v3.3] Entropic vortex coil created.")
