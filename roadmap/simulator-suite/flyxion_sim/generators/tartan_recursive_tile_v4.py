from __future__ import annotations
import random
from flyxion_sim.core import GeneratorSpec, register, make_material

def build(config, params):
    import bpy
    random.seed(params.get("seed", config.seed))
    depth=params.get("depth", 3); tile_size=params.get("tile_size", .72)
    base_mat=make_material("Mat_TARTAN_v4_Base", (.08,.1,.14,1), None, 0, .82)
    glow=make_material("Mat_TARTAN_v4_Corners", (.9,.8,.4,1), (.9,.8,.4,1), 4.5)
    bpy.ops.mesh.primitive_cube_add(size=3.2, location=(0,0,0)); bpy.context.active_object.name="TARTAN_v4_BaseCube"; bpy.context.active_object.data.materials.append(base_mat)
    offsets=range(-depth, depth+1)
    for axis in range(3):
        for i in offsets:
            for j in offsets:
                loc=[i*tile_size,j*tile_size,1.75]
                if axis==0: loc=(1.75,i*tile_size,j*tile_size)
                elif axis==1: loc=(i*tile_size,1.75,j*tile_size)
                else: loc=(i*tile_size,j*tile_size,1.75)
                bpy.ops.mesh.primitive_cube_add(size=tile_size*.82, location=loc)
                obj=bpy.context.active_object; obj.name=f"TARTAN_v4_Tile_{axis}_{i}_{j}"
                col=(.15+random.random()*.55,.35+random.random()*.25,.55+random.random()*.4,1)
                obj.data.materials.append(make_material(f"Mat_{obj.name}", col, (col[0]*.4,col[1]*.4,col[2]*.4,1), 1.8))
    for sx in (-1,1):
        for sy in (-1,1):
            for sz in (-1,1):
                bpy.ops.mesh.primitive_uv_sphere_add(radius=.35, location=(1.95*sx,1.95*sy,1.95*sz))
                bpy.context.active_object.name=f"TARTAN_v4_Corner_{sx}_{sy}_{sz}"; bpy.context.active_object.data.materials.append(glow)

register(GeneratorSpec("tartan_recursive_tile", "TARTAN", "Recursive face tiling cube with corner semantic anchors.", build, {"depth": 3}))
