from flyxion_sim.core import GeneratorSpec, register, make_material, bezier_tube
import math, random

def build(config, params):
    import bpy
    random.seed(params.get("seed", config.seed)); n=params.get("neurons", 14)
    trunk=make_material("Mat_Xylo_v4_Trunk", (.2,.3,.23,1), None, 0, .85)
    glow=make_material("Mat_Xylo_v4_Neurons", (.25,.9,.7,1), (.25,.9,.7,1), 7)
    tube=make_material("Mat_Xylo_v4_Tubes", (.35,.7,.4,1), (.2,.7,.4,1), 3)
    bpy.ops.mesh.primitive_cylinder_add(radius=.72, depth=10, location=(0,0,5)); bpy.context.active_object.name="Xylo_v4_Spine"; bpy.context.active_object.data.materials.append(trunk)
    locs=[]
    for i in range(n):
        a=2*math.pi*i/n; r=4+random.uniform(-.7,.7); loc=(r*math.cos(a), r*math.sin(a), 10+random.uniform(-.5,.9)); locs.append(loc)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=.5+random.random()*.18, location=loc); bpy.context.active_object.name=f"Xylo_v4_Neuron_{i:02d}"; bpy.context.active_object.data.materials.append(glow)
        bezier_tube(f"Xylo_v4_Root_{i:02d}", [(0,0,8), (loc[0]*.45,loc[1]*.45,9.5), loc], .08, tube)
    for i in range(0,n,2):
        bezier_tube(f"Xylo_v4_CrossBridge_{i:02d}", [locs[i], ((locs[i][0]+locs[(i+1)%n][0])/2,(locs[i][1]+locs[(i+1)%n][1])/2,11.5), locs[(i+1)%n]], .055, tube)

register(GeneratorSpec("xylomorphic_root_brain", "Xylomorphic", "Root-trunk-neuron hybrid: plant morphology as cognitive graph.", build, {"neurons": 14}))
