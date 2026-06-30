from flyxion_sim.core import GeneratorSpec, register, make_material, cylinder_between
import math

def build(config, params):
    import bpy
    radius=params.get("orbit_radius", 3.3)
    core_mat=make_material("Mat_Semantic_v4_Core", (.4,.9,.9,1), (.4,.9,.9,1), 5)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=(0,0,0)); core=bpy.context.active_object; core.name="Semantic_v4_Core"; core.data.materials.append(core_mat)
    specs=[("Plus",0,6,(.9,.6,.3,1)),("Tensor",math.pi/2,None,(.5,.6,1,1)),("Implies",math.pi,None,(.9,.4,.7,1)),("Mu",3*math.pi/2,None,(.6,1,.7,1))]
    link_mat=make_material("Mat_Semantic_v4_Orbit_Links", (.8,.8,1,1), (.8,.8,1,1), 2.8)
    prev=None; first=None
    for name,ang,verts,col in specs:
        loc=(radius*math.cos(ang), radius*math.sin(ang), .6+0.5*math.sin(2*ang))
        if name=="Plus": bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=.45, depth=.65, location=loc)
        elif name=="Tensor": bpy.ops.mesh.primitive_torus_add(major_radius=.55, minor_radius=.12, location=loc)
        elif name=="Implies": bpy.ops.mesh.primitive_cube_add(size=.55, location=loc); bpy.context.active_object.scale=(.5,1.8,.5)
        else: bpy.ops.mesh.primitive_uv_sphere_add(radius=.55, location=loc)
        obj=bpy.context.active_object; obj.name=f"Semantic_v4_Operator_{name}"; obj.data.materials.append(make_material(f"Mat_{obj.name}", col, col, 4.5))
        cylinder_between((0,0,0), loc, .035, f"Semantic_v4_Spoke_{name}", link_mat)
        if prev is not None: cylinder_between(prev, loc, .03, "Semantic_v4_Orbit_Segment", link_mat)
        else: first=loc
        prev=loc
    cylinder_between(prev, first, .03, "Semantic_v4_Orbit_Segment", link_mat)

register(GeneratorSpec("semantic_operator_orbit", "Semantic Geometry", "Orbit of algebraic operators around a semantic core.", build, {}))
