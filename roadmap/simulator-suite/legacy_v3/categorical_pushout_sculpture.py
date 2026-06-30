import bpy

# Clear
for obj in list(bpy.context.scene.objects):
    if obj.type in {'MESH', 'CURVE'}:
        bpy.data.objects.remove(obj, do_unlink=True)

def block(name, loc, color):
    bpy.ops.mesh.primitive_cube_add(size=1.4, location=loc)
    obj = bpy.context.active_object
    obj.name = name
    m = bpy.data.materials.new(f"Mat_{name}")
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Emission"].default_value = (color[0]*0.5,color[1]*0.5,color[2]*0.5,1.0)
    bsdf.inputs["Emission Strength"].default_value = 2.5
    obj.data.materials.append(m)
    return obj

def arrow(start, end, name):
    import mathutils
    start_v = mathutils.Vector(start)
    end_v = mathutils.Vector(end)
    direction = end_v - start_v
    length = direction.length
    direction.normalize()

    bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=length*0.7, location=(0,0,0))
    cyl = bpy.context.active_object
    bpy.ops.mesh.primitive_cone_add(radius1=0.16, depth=length*0.3, location=(0,0,0))
    cone = bpy.context.active_object
    cone.parent = cyl

    up = mathutils.Vector((0,0,1))
    rot = up.rotation_difference(direction)
    cyl.rotation_mode = 'QUATERNION'
    cone.rotation_mode = 'QUATERNION'
    cyl.rotation_quaternion = rot
    cone.rotation_quaternion = rot

    mid = (start_v + end_v) / 2
    cyl.location = mid
    cone.location = end_v

    for obj in (cyl, cone):
        obj.name = f"{name}_{obj.name}"
        m = bpy.data.materials.new(f"Mat_{name}")
        m.use_nodes = True
        bsdf = m.node_tree.nodes["Principled BSDF"]
        bsdf.inputs["Emission"].default_value = (0.9,0.9,1.0,1.0)
        bsdf.inputs["Emission Strength"].default_value = 5.0
        obj.data.materials.append(m)

# Objects A,B,C,D forming a pushout-ish diagram
A = block("Obj_A", (-3, 2, 0.7), (0.3,0.7,1.0,1.0))
B = block("Obj_B", ( 3, 2, 0.7), (1.0,0.5,0.3,1.0))
C = block("Obj_C", (-3,-2,0.7), (0.4,1.0,0.6,1.0))
D = block("Obj_D", ( 3,-2,0.7), (0.9,0.9,0.9,1.0))

arrow((-3,2,0.7), (3,2,0.7), "f")
arrow((-3,-2,0.7), (-3,2,0.7), "g")
arrow((3,-2,0.7), (3,2,0.7), "h")
arrow((-3,-2,0.7), (3,-2,0.7), "p")

print("[v3.3] Categorical pushout sculpture created.")
