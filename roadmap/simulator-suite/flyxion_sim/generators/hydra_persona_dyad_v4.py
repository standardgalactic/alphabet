from flyxion_sim.core import GeneratorSpec, register, make_material, bezier_tube

def build(config, params):
    import bpy
    data=[("Seer",(.4,.8,1,1),(-3,0,0)),("Engineer",(.4,1,.4,1),(3,0,0))]
    for name,col,loc in data:
        bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=1, depth=.35, location=loc); obj=bpy.context.active_object; obj.name=f"Dyad_v4_{name}_Glyph"; obj.data.materials.append(make_material(f"Mat_Dyad_{name}", col, col,4))
    bezier_tube("Dyad_v4_Bond", [(-3,0,.5),(0,0,2.7),(3,0,.5)], .11, make_material("Mat_Dyad_Bond", (.9,.9,1,1),(.9,.9,1,1),5))
register(GeneratorSpec("hydra_persona_dyad", "HYDRA", "Two-persona coordination glyph linked by a shared bond.", build, {}))
