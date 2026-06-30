import bpy
import math
import random
import mathutils

# Clear
for obj in list(bpy.context.scene.objects):
    if obj.type in {'MESH', 'CURVE'}:
        bpy.data.objects.remove(obj, do_unlink=True)

random.seed(99)

# Spine
bpy.ops.mesh.primitive_cylinder_add(radius=0.7, depth=10.0, location=(0.0, 0.0, 5.0))
spine = bpy.context.active_object
spine.name = "RootBrain_Spine"
sm = bpy.data.materials.new("Mat_Spine")
sm.use_nodes = True
sbsdf = sm.node_tree.nodes["Principled BSDF"]
sbsdf.inputs["Base Color"].default_value = (0.2, 0.3, 0.23,1.0)
sbsdf.inputs["Roughness"].default_value = 0.8
spine.data.materials.append(sm)

# Canopy neuron nodes at top
top = spine.location + mathutils.Vector((0,0,5.0))
neuron_locs = []
for i in range(10):
    ang = 2*math.pi*i/10
    r = 4.0 + random.uniform(-0.5,0.5)
    x = top.x + r*math.cos(ang)
    y = top.y + r*math.sin(ang)
    z = top.z + random.uniform(-0.5,0.8)
    neuron_locs.append((x,y,z))
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.6, location=(x,y,z))
    neu = bpy.context.active_object
    neu.name = f"Neuron_{i}"
    nm = bpy.data.materials.new(f"Mat_Neuron_{i}")
    nm.use_nodes = True
    bsdf = nm.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Emission"].default_value = (0.25, 0.9, 0.7,1.0)
    bsdf.inputs["Emission Strength"].default_value = 7.0
    neu.data.materials.append(nm)

# Mycelial tubes from spine to neurons
def make_tube(start, end, name):
    curve_data = bpy.data.curves.new(name, 'CURVE')
    curve_data.dimensions = '3D'
    spline = curve_data.splines.new('BEZIER')
    spline.bezier_points.add(2)
    p0,p1,p2 = spline.bezier_points
    p0.co = start
    mid = (mathutils.Vector(start)+mathutils.Vector(end))/2 + mathutils.Vector((0,0,1.0))
    p1.co = mid
    p2.co = end
    for p in spline.bezier_points:
        p.handle_left_type = p.handle_right_type = 'AUTO'
    curve_data.bevel_depth = 0.1
    obj = bpy.data.objects.new(name, curve_data)
    bpy.context.scene.collection.objects.link(obj)
    m = bpy.data.materials.new(f"Mat_{name}")
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.35,0.7,0.4,1.0)
    bsdf.inputs["Emission"].default_value = (0.2,0.7,0.4,1.0)
    bsdf.inputs["Emission Strength"].default_value = 3.0
    curve_data.materials.append(m)

for loc in neuron_locs:
    make_tube((0.0,0.0,8.0), loc, "RootBrain_Tube")

# Cross-cortical bridges
for i in range(0,len(neuron_locs),2):
    if i+1 < len(neuron_locs):
        make_tube(neuron_locs[i], neuron_locs[i+1], "RootBrain_Bridge")

print("[v3.3] Xylomorphic root-brain created.")
