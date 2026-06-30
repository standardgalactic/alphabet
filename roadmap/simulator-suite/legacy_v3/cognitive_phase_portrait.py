import bpy
import random
import math

# Clear
for obj in list(bpy.context.scene.objects):
    if obj.type in {'MESH', 'CURVE'}:
        bpy.data.objects.remove(obj, do_unlink=True)

random.seed(7)

# Attractor points
attractors = [
    (0,0,0.2),
    (4,4,0.2),
    (-4,3,0.2),
    (-3,-4,0.2),
]

for idx, loc in enumerate(attractors):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.4, location=loc)
    a = bpy.context.active_object
    a.name = f"Attractor_{idx}"
    m = bpy.data.materials.new(f"Mat_Attractor_{idx}")
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Emission"].default_value = (0.9,0.9,0.5,1.0)
    bsdf.inputs["Emission Strength"].default_value = 5.0
    a.data.materials.append(m)

# Flow arrows toward attractors
for i in range(80):
    x = random.uniform(-6,6)
    y = random.uniform(-6,6)
    z = random.uniform(0.0,3.0)

    # choose nearest attractor
    import mathutils
    p = mathutils.Vector((x,y,z))
    best = None
    best_d = 999.0
    for loc in attractors:
        d = (p - mathutils.Vector(loc)).length
        if d < best_d:
            best_d = d
            best = loc

    dir_vec = mathutils.Vector(best) - p
    length = dir_vec.length
    if length < 0.1:
        continue
    dir_vec.normalize()

    bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=length*0.7, location=(0,0,0))
    cyl = bpy.context.active_object
    bpy.ops.mesh.primitive_cone_add(radius1=0.1, depth=length*0.3, location=(0,0,0))
    cone = bpy.context.active_object
    cone.parent = cyl

    up = mathutils.Vector((0,0,1))
    rot = up.rotation_difference(dir_vec)
    cyl.rotation_mode = 'QUATERNION'
    cone.rotation_mode = 'QUATERNION'
    cyl.rotation_quaternion = rot
    cone.rotation_quaternion = rot

    mid = (p + mathutils.Vector(best))/2
    cyl.location = mid
    cone.location = best

    for obj in (cyl, cone):
        obj.name = "FlowArrow"
        m = bpy.data.materials.new("Mat_FlowArrow")
        m.use_nodes = True
        bsdf = m.node_tree.nodes["Principled BSDF"]
        bsdf.inputs["Emission"].default_value = (0.4,0.7,1.0,1.0)
        bsdf.inputs["Emission Strength"].default_value = 3.0
        obj.data.materials.append(m)

print("[v3.3] Cognitive phase portrait created.")
