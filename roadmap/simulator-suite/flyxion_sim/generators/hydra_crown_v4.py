from flyxion_sim.core import GeneratorSpec, register, make_material, bezier_tube
import math

def build(config, params):
    import bpy
    personas=params.get("personas", ["Seer","Engineer","Archivist","Trickster","Repairer","Cartographer"])
    colors=[(.4,.8,1,1),(.4,1,.4,1),(1,.7,.3,1),(1,.3,.7,1),(.9,.9,.5,1),(.6,.7,1,1)]
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.05, location=(0,0,0)); core=bpy.context.active_object; core.name="HYDRA_v4_Crown_Core"; core.data.materials.append(make_material("Mat_HYDRA_v4_Core", (.3,.9,.9,1), (.3,.9,.9,1), 7))
    for idx,name in enumerate(personas):
        ang=2*math.pi*idx/len(personas); x=3.3*math.cos(ang); y=3.3*math.sin(ang); z=1.0+0.35*((idx%2)*2-1)
        bpy.ops.mesh.primitive_cone_add(radius1=.55, depth=1.55, location=(x,y,z)); spike=bpy.context.active_object; spike.name=f"HYDRA_v4_{name}_Spike"; spike.rotation_euler[2]=ang+math.pi/2
        col=colors[idx%len(colors)]; spike.data.materials.append(make_material(f"Mat_HYDRA_v4_{name}", col, col, 5))
        bezier_tube(f"HYDRA_v4_Link_{name}", [(0,0,.5),(x*.55,y*.55,1.8),(x,y,z)], .055, make_material(f"Mat_HYDRA_v4_Link_{name}", (.8,.8,1,1), (.8,.8,1,1), 4))

register(GeneratorSpec("hydra_crown", "HYDRA", "Multi-persona crown around a shared coordination core.", build, {}))
