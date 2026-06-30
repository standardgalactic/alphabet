from flyxion_sim.core import GeneratorSpec, register, make_material
import math

def build(config, params):
    import bpy
    turns=params.get("turns",4); ribbons=params.get("ribbons",5); height=params.get("height",8.5); radius=params.get("radius",3.0)
    for j in range(ribbons):
        curve=bpy.data.curves.new(f"Vortex_v4_Ribbon_{j}",'CURVE'); curve.dimensions='3D'; sp=curve.splines.new('POLY'); steps=96; sp.points.add(steps-1); phase=2*math.pi*j/ribbons
        for i in range(steps):
            t=i/(steps-1); a=2*math.pi*turns*t+phase; r=radius+.35*math.sin(4*a+j); sp.points[i].co=(r*math.cos(a),r*math.sin(a),height*(t-.5),1)
        curve.bevel_depth=.1; obj=bpy.data.objects.new(f"Vortex_v4_Ribbon_{j}",curve); bpy.context.scene.collection.objects.link(obj)
        col=(.35+.1*j,.6,1-.08*j,1); curve.materials.append(make_material(f"Mat_Vortex_v4_{j}", col, col,5))
    bpy.ops.mesh.primitive_cylinder_add(radius=.45, depth=height+1, location=(0,0,0)); bpy.context.active_object.name="Vortex_v4_Core"; bpy.context.active_object.data.materials.append(make_material("Mat_Vortex_v4_Core", (.9,.9,1,1),(.9,.9,1,1),4))
register(GeneratorSpec("entropic_vortex_coil", "Entropy", "Helical entropy ribbons around a stabilizing core.", build, {}))
