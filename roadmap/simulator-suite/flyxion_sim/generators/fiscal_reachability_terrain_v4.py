from flyxion_sim.core import GeneratorSpec, register, make_material
import math, random

def build(config, params):
    import bpy
    random.seed(params.get("seed", config.seed)); n=params.get("grid", 13)
    mat=make_material("Mat_Fiscal_v4_Terrain", (.2,.45,.8,1),(.05,.15,.35,1),1.2)
    danger=make_material("Mat_Fiscal_v4_Boundary", (1,.25,.2,1),(1,.1,.05,1),4)
    for i in range(n):
        for j in range(n):
            x=(i-n/2)*.65; y=(j-n/2)*.65; h=1.5+math.sin(i*.7)*.5+math.cos(j*.6)*.5-0.08*((i-n/2)**2+(j-n/2)**2)
            bpy.ops.mesh.primitive_cube_add(size=.5, location=(x,y,h/2)); obj=bpy.context.active_object; obj.name=f"Fiscal_v4_Cell_{i}_{j}"; obj.scale.z=max(.1,h); obj.data.materials.append(danger if h<.6 else mat)

register(GeneratorSpec("fiscal_reachability_terrain", "Reachability", "Fiscal capacity surface with boundary-fragile low regions.", build, {"grid":13}))
