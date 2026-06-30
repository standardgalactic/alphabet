from flyxion_sim.core import GeneratorSpec, register, make_material, bezier_tube
import math

def build(config, params):
    import bpy
    strands=params.get("strands", 7)
    mats=[make_material("Mat_Repair_v4_Wound", (1,.2,.25,1),(1,.1,.1,1),5), make_material("Mat_Repair_v4_Trace", (.5,.9,1,1),(.5,.9,1,1),4)]
    for j in range(strands):
        pts=[]
        for i in range(50):
            t=i/49; x=-5+10*t; y=(j-strands/2)*.35+math.sin(t*math.pi*4+j)*.25; z=1+math.cos(t*math.pi*2+j)*.6
            pts.append((x,y,z))
        bezier_tube(f"Repair_v4_Trace_{j}", [pts[0], pts[16], pts[32], pts[-1]], .045, mats[1])
    bpy.ops.mesh.primitive_uv_sphere_add(radius=.8, location=(0,0,1)); bpy.context.active_object.name="Repair_v4_Rupture_Node"; bpy.context.active_object.data.materials.append(mats[0])

register(GeneratorSpec("repair_trace_weaver", "Repair", "A rupture crossed by multiple continuation traces.", build, {"strands":7}))
