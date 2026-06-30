import bpy
import math
import random

# Clear meshes & curves
for obj in list(bpy.context.scene.objects):
    if obj.type in {"MESH", "CURVE"}:
        bpy.data.objects.remove(obj, do_unlink=True)

# Base cube
bpy.ops.mesh.primitive_cube_add(size=3.0, location=(0, 0, 0))
base = bpy.context.active_object
base.name = "TARTAN_BaseCube"
bm = bpy.data.materials.new("Mat_TARTAN_Base")
bm.use_nodes = True
bbsdf = bm.node_tree.nodes["Principled BSDF"]
bbsdf.inputs["Base Color"].default_value = (0.1, 0.15, 0.2, 1.0)
bbsdf.inputs["Roughness"].default_value = 0.8
base.data.materials.append(bm)

# Face sub-tiles
offsets = [-1, 0, 1]
tile_size = 0.8
for axis in range(3):
    for i in offsets:
        for j in offsets:
            if axis == 0:
                loc = (1.6, i*tile_size, j*tile_size)
            elif axis == 1:
                loc = (i*tile_size, 1.6, j*tile_size)
            else:
                loc = (i*tile_size, j*tile_size, 1.6)
            bpy.ops.mesh.primitive_cube_add(size=tile_size, location=loc)
            c = bpy.context.active_object
            c.name = f"TARTAN_Tile_{axis}_{i}_{j}"
            cm = bpy.data.materials.new(f"Mat_Tile_{axis}_{i}_{j}")
            cm.use_nodes = True
            col = (0.2 + random.random()*0.5, 0.4, 0.6 + random.random()*0.4, 1.0)
            bsdf = cm.node_tree.nodes["Principled BSDF"]
            bsdf.inputs["Base Color"].default_value = col
            bsdf.inputs["Emission"].default_value = (col[0]*0.5, col[1]*0.5, col[2]*0.5, 1.0)
            bsdf.inputs["Emission Strength"].default_value = 1.5
            c.data.materials.append(cm)

# Corner semantic nodes
for sx in (-1, 1):
    for sy in (-1, 1):
        for sz in (-1, 1):
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.4, location=(1.8*sx,1.8*sy,1.8*sz))
            node = bpy.context.active_object
            node.name = f"TARTAN_Corner_{sx}_{sy}_{sz}"
            nm = bpy.data.materials.new(f"Mat_Corner_{sx}_{sy}_{sz}")
            nm.use_nodes = True
            bsdf = nm.node_tree.nodes["Principled BSDF"]
            bsdf.inputs["Emission"].default_value = (0.9, 0.8, 0.4, 1.0)
            bsdf.inputs["Emission Strength"].default_value = 4.0
            node.data.materials.append(nm)

print("[v3.3] TARTAN recursive tile created.")
