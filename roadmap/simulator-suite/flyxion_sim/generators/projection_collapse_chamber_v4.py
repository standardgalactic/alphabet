from flyxion_sim.core import GeneratorSpec, register, make_material, cylinder_between
import math

def build(config, params):
    import bpy
    high=make_material("Mat_CLIO_v4_High", (.4,.8,1,1),(.2,.6,1,1),3)
    low=make_material("Mat_CLIO_v4_Collapse", (1,.55,.25,1),(1,.35,.1,1),4)
    for i in range(18):
        a=2*math.pi*i/18; loc=(3*math.cos(a),3*math.sin(a),1.8*math.sin(3*a)+1.5)
        bpy.ops.mesh.primitive_ico_sphere_add(radius=.18, location=loc); bpy.context.active_object.name=f"CLIO_v4_Preimage_{i}"; bpy.context.active_object.data.materials.append(high)
        target=(1.1*math.cos(a),1.1*math.sin(a),-.8)
        cylinder_between(loc,target,.025,"CLIO_v4_Projection_Ray",high)
    bpy.ops.mesh.primitive_torus_add(major_radius=1.15, minor_radius=.12, location=(0,0,-.8)); bpy.context.active_object.name="CLIO_v4_Collapse_Quotient"; bpy.context.active_object.data.materials.append(low)

register(GeneratorSpec("projection_collapse_chamber", "CLIO", "Many high-dimensional distinctions projected into a lower quotient ring.", build, {}))
