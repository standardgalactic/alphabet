import bpy
import random

# Clear meshes & curves
for obj in list(bpy.context.scene.objects):
    if obj.type in {"MESH", "CURVE"}:
        bpy.data.objects.remove(obj, do_unlink=True)

# Φ core
bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=(0, 0, 0))
phi = bpy.context.active_object
phi.name = "Hypercell_Phi_Core"
m = bpy.data.materials.new("Mat_Hyper_Phi")
m.use_nodes = True
bsdf = m.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Emission"].default_value = (0.3, 0.9, 1.0, 1.0)
bsdf.inputs["Emission Strength"].default_value = 7.0
phi.data.materials.append(m)

# Vector shell (anisotropic)
bpy.ops.mesh.primitive_uv_sphere_add(radius=1.4, location=(0, 0, 0))
vs = bpy.context.active_object
vs.name = "Hypercell_Vector_Shell"
vs.scale = (1.5, 1.1, 1.3)
vm = bpy.data.materials.new("Mat_Hyper_Vector")
vm.use_nodes = True
vbsdf = vm.node_tree.nodes["Principled BSDF"]
vbsdf.inputs["Base Color"].default_value = (1.0, 0.6, 0.3, 0.6)
vbsdf.inputs["Transmission"].default_value = 0.4
vbsdf.inputs["Roughness"].default_value = 0.15
vs.data.materials.append(vm)

# Coherence shell (smooth translucent bubble)
bpy.ops.mesh.primitive_uv_sphere_add(radius=1.8, location=(0, 0, 0))
coh = bpy.context.active_object
coh.name = "Hypercell_Coherence_Shell"
cm = bpy.data.materials.new("Mat_Hyper_Coh")
cm.use_nodes = True
cbsdf = cm.node_tree.nodes["Principled BSDF"]
cbsdf.inputs["Base Color"].default_value = (0.8, 0.9, 1.0, 0.3)
cbsdf.inputs["Transmission"].default_value = 0.7
cbsdf.inputs["Roughness"].default_value = 0.1
coh.data.materials.append(cm)

# Entropy sparks
ENTROPY_SPARK_COLOR = (1.0, 0.2, 0.5, 1.0)
for i in range(80):
    import math
    theta = random.random() * math.pi
    phi_ang = random.random() * 2 * math.pi
    r = 2.2 + random.uniform(-0.1, 0.2)
    x = r * math.sin(theta) * math.cos(phi_ang)
    y = r * math.sin(theta) * math.sin(phi_ang)
    z = r * math.cos(theta)
    bpy.ops.mesh.primitive_ico_sphere_add(radius=0.12, location=(x, y, z))
    s = bpy.context.active_object
    s.name = f"Hyper_Entropy_Spark_{i}"
    sm = bpy.data.materials.new(f"Mat_Hyper_Spark_{i}")
    sm.use_nodes = True
    sbsdf = sm.node_tree.nodes["Principled BSDF"]
    sbsdf.inputs["Emission"].default_value = ENTROPY_SPARK_COLOR
    sbsdf.inputs["Emission Strength"].default_value = 9.0
    s.data.materials.append(sm)

# Constraint cage (wireframe icosphere)
bpy.ops.mesh.primitive_ico_sphere_add(radius=2.4, subdivisions=2, location=(0, 0, 0))
cage = bpy.context.active_object
cage.name = "Hypercell_Constraint_Cage"
mod = cage.modifiers.new("Wire", type='WIREFRAME')
mod.thickness = 0.04
mm = bpy.data.materials.new("Mat_Hyper_Cage")
mm.use_nodes = True
mbsdf = mm.node_tree.nodes["Principled BSDF"]
mbsdf.inputs["Emission"].default_value = (0.6, 0.8, 1.0, 1.0)
mbsdf.inputs["Emission Strength"].default_value = 4.0
cage.data.materials.append(mm)

print("[v3.3] RSVP Hypercell created.")
