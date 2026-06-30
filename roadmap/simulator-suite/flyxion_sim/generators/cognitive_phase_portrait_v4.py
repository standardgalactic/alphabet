from flyxion_sim.core import GeneratorSpec, register, make_material, cylinder_between
import random, math

def build(config, params):
    import bpy, mathutils
    random.seed(params.get("seed", config.seed)); count=params.get("arrows", 90)
    attractors=[(0,0,.2),(4,4,.2),(-4,3,.2),(-3,-4,.2)]
    amat=make_material("Mat_Phase_v4_Attractors", (.9,.9,.5,1),(.9,.9,.5,1),5); fmat=make_material("Mat_Phase_v4_Flow", (.4,.7,1,1),(.4,.7,1,1),3)
    for i,loc in enumerate(attractors): bpy.ops.mesh.primitive_uv_sphere_add(radius=.4, location=loc); bpy.context.active_object.name=f"Phase_v4_Attractor_{i}"; bpy.context.active_object.data.materials.append(amat)
    for i in range(count):
        p=(random.uniform(-6,6),random.uniform(-6,6),random.uniform(0,3)); best=min(attractors,key=lambda q:sum((p[k]-q[k])**2 for k in range(3)))
        cylinder_between(p,best,.035,"Phase_v4_FlowArrow",fmat)
register(GeneratorSpec("cognitive_phase_portrait", "Cognition", "Local arrows falling into cognitive attractor basins.", build, {"arrows":90}))
