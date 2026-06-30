from flyxion_sim.core import GeneratorSpec, register, make_material, cylinder_between
import random

def build(config, params):
    import bpy
    random.seed(params.get("seed", config.seed)); n=params.get("events", 24)
    event=make_material("Mat_MEM8_v4_Event", (.9,.8,.45,1),(.9,.7,.25,1),4)
    line=make_material("Mat_MEM8_v4_LogLine", (.65,.8,1,1),(.5,.7,1,1),2.5)
    prev=None
    for i in range(n):
        loc=(-6+i*.52, random.uniform(-1.4,1.4), .2+random.uniform(0,2.6))
        bpy.ops.mesh.primitive_cube_add(size=.26+random.random()*.18, location=loc); obj=bpy.context.active_object; obj.name=f"MEM8_v4_Event_{i:03d}"; obj.data.materials.append(event)
        if prev: cylinder_between(prev, loc, .025, "MEM8_v4_Recoverability_Link", line)
        prev=loc

register(GeneratorSpec("memory_event_log", "MEM|8", "Recoverability as a chain of situated events rather than stored images.", build, {"events":24}))
