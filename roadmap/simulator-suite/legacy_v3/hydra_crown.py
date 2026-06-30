import bpy
import math

# Clear
for obj in list(bpy.context.scene.objects):
    if obj.type in {'MESH', 'CURVE'}:
        bpy.data.objects.remove(obj, do_unlink=True)

# Central core
bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=(0,0,0))
core = bpy.context.active_object
core.name = "HYDRA_Crown_Core"
cm = bpy.data.materials.new("Mat_HC_Core")
cm.use_nodes = True
bsdf = cm.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Emission"].default_value = (0.3,0.9,0.9,1.0)
bsdf.inputs["Emission Strength"].default_value = 6.0
core.data.materials.append(cm)

personas = [
    ("Seer",      (0.4,0.8,1.0,1.0)),
    ("Engineer",  (0.4,1.0,0.4,1.0)),
    ("Archivist", (1.0,0.7,0.3,1.0)),
    ("Trickster", (1.0,0.3,0.7,1.0)),
]

radius = 3.0
for idx,(name,color) in enumerate(personas):
    ang = 2*math.pi*idx/len(personas)
    x = radius*math.cos(ang)
    y = radius*math.sin(ang)
    z = 1.0
    bpy.ops.mesh.primitive_cone_add(radius1=0.6, depth=1.5, location=(x,y,z))
    cone = bpy.context.active_object
    cone.name = f"HC_{name}_Spike"
    cone.rotation_euler[2] = ang + math.pi/2
    m = bpy.data.materials.new(f"Mat_HC_{name}")
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Emission"].default_value = color
    bsdf.inputs["Emission Strength"].default_value = 5.0
    cone.data.materials.append(m)

    # link ribbon to core
    curve_data = bpy.data.curves.new(f"HC_Link_{name}", 'CURVE')
    curve_data.dimensions = '3D'
    spline = curve_data.splines.new('BEZIER')
    spline.bezier_points.add(1)
    p0,p1 = spline.bezier_points
    p0.co = (0,0,0.5)
    p1.co = (x,y,1.0)
    for p in spline.bezier_points:
        p.handle_left_type = p.handle_right_type = 'AUTO'
    curve_data.bevel_depth = 0.07
    robj = bpy.data.objects.new(f"HC_Link_{name}", curve_data)
    bpy.context.scene.collection.objects.link(robj)
    lm = bpy.data.materials.new(f"Mat_HC_Link_{name}")
    lm.use_nodes = True
    lbsdf = lm.node_tree.nodes["Principled BSDF"]
    lbsdf.inputs["Emission"].default_value = (0.8,0.8,1.0,1.0)
    lbsdf.inputs["Emission Strength"].default_value = 4.0
    curve_data.materials.append(lm)

print("[v3.3] HYDRA crown created.")
