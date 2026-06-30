from flyxion_sim.core import GeneratorSpec, register, make_material, cylinder_between

def build(config, params):
    import bpy
    pos={"A":(-3,2,.7),"B":(3,2,.7),"C":(-3,-2,.7),"D":(3,-2,.7)}
    cols={"A":(.3,.7,1,1),"B":(1,.5,.3,1),"C":(.4,1,.6,1),"D":(.9,.9,.9,1)}
    for k,loc in pos.items():
        bpy.ops.mesh.primitive_cube_add(size=1.35, location=loc); obj=bpy.context.active_object; obj.name=f"Pushout_v4_Object_{k}"; obj.data.materials.append(make_material(f"Mat_Pushout_{k}", cols[k], cols[k], 2.5))
    arrow=make_material("Mat_Pushout_v4_Arrows", (.9,.9,1,1),(.9,.9,1,1),4)
    for s,t,n in [("A","B","f"),("C","A","g"),("D","B","h"),("C","D","p")]: cylinder_between(pos[s],pos[t],.07,f"Pushout_v4_Arrow_{n}",arrow)
register(GeneratorSpec("categorical_pushout_sculpture", "Category Theory", "Commutative square as sculptural pushout object.", build, {}))
