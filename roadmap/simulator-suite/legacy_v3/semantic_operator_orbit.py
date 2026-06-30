import bpy
import math

# Clear
for obj in list(bpy.context.scene.objects):
    if obj.type in {"MESH", "CURVE"}:
        bpy.data.objects.remove(obj, do_unlink=True)

# Core
bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=(0,0,0))
core = bpy.context.active_object
core.name = "Semantic_Core"
cm = bpy.data.materials.new("Mat_Semantic_Core")
cm.use_nodes = True
bsdf = cm.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Emission"].default_value = (0.4, 0.9, 0.9, 1.0)
bsdf.inputs["Emission Strength"].default_value = 5.0
core.data.materials.append(cm)

# Operator shapes
# ⊕ -> hexagonal prism
bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.4, depth=0.6, location=(3.0, 0.0, 0.3))
op_plus = bpy.context.active_object
op_plus.name = "Op_MonoidalPlus"

# ⊗ -> torus knot-like torus
bpy.ops.mesh.primitive_torus_add(major_radius=3.2, minor_radius=0.15, location=(0.0,0.0,0.0))
op_tensor = bpy.context.active_object
op_tensor.name = "Op_TensorLoop"

# ⇒ -> long crystal (elongated cube)
bpy.ops.mesh.primitive_cube_add(size=0.4, location=(0.0, 3.0, 1.2))
op_imp = bpy.context.active_object
op_imp.scale = (0.4, 1.6, 0.4)
op_imp.name = "Op_Implies"

# μ -> glowing sphere
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(-3.0,0.0,0.5))
op_mu = bpy.context.active_object
op_mu.name = "Op_Mu"

ops = [
    (op_plus, (0.9, 0.6, 0.3, 1.0)),
    (op_tensor, (0.5, 0.6, 1.0, 1.0)),
    (op_imp, (0.9, 0.4, 0.7, 1.0)),
    (op_mu, (0.6, 1.0, 0.7, 1.0)),
]

for obj, col in ops:
    m = bpy.data.materials.new(f"Mat_{obj.name}")
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Emission"].default_value = col
    bsdf.inputs["Emission Strength"].default_value = 4.0
    bsdf.inputs["Base Color"].default_value = col
    obj.data.materials.append(m)

print("[v3.3] Semantic operator orbit created.")
