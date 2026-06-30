from flyxion_sim.core import GeneratorSpec, register, make_material, cylinder_between
import math, random

def build(config, params):
    import bpy
    random.seed(params.get("seed", config.seed)); size=params.get("size", 5)
    ok=make_material("Mat_Admissible_v4", (.35,1,.65,1), (.2,.7,.4,1), 2.5)
    bad=make_material("Mat_Refused_v4", (1,.25,.35,1), (1,.1,.2,1), 4.0)
    edge=make_material("Mat_Boundary_v4_Edge", (.8,.85,1,1), (.8,.85,1,1), 2.0)
    points=[]
    for x in range(-size,size+1,2):
        for y in range(-size,size+1,2):
            z=.5*math.sin(x*.8)+.5*math.cos(y*.8)
            admissible=(x*x+y*y+3*z*z) < size*size*.8
            bpy.ops.mesh.primitive_ico_sphere_add(radius=.18 if admissible else .26, location=(x,y,z))
            obj=bpy.context.active_object; obj.name=("Admissible" if admissible else "Refused")+f"_State_{x}_{y}"; obj.data.materials.append(ok if admissible else bad)
            points.append(((x,y,z), admissible))
    for i,(p,a) in enumerate(points):
        for q,b in points[i+1:]:
            if sum((p[k]-q[k])**2 for k in range(3)) <= 4.2 and a and b:
                cylinder_between(p,q,.025,"Admissibility_v4_Reachability_Edge",edge)

register(GeneratorSpec("admissibility_boundary_lattice", "Admissibility", "Discrete state lattice with refused boundary and reachable interior.", build, {"size":5}))
