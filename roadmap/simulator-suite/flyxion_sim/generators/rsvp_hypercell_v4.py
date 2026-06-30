from __future__ import annotations
import math, random
from flyxion_sim.core import GeneratorSpec, register, make_material

def build(config, params):
    import bpy
    random.seed(params.get("seed", config.seed))
    core_radius = params.get("core_radius", 1.0)
    spark_count = params.get("spark_count", 120)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=core_radius, location=(0,0,0))
    core = bpy.context.active_object; core.name = "RSVP_v4_Phi_Core"
    core.data.materials.append(make_material("Mat_RSVP_v4_Phi", (0.3,0.9,1.0,1), (0.3,0.9,1.0,1), 8.0))
    for radius, scale, name, col, alpha in [(1.45,(1.6,1.05,1.3),"Vector_Shell",(1.0,0.6,0.3,0.45),0.45),(1.95,(1,1,1),"Coherence_Shell",(0.8,0.9,1.0,0.25),0.25)]:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=(0,0,0))
        obj=bpy.context.active_object; obj.name=f"RSVP_v4_{name}"; obj.scale=scale
        obj.data.materials.append(make_material(f"Mat_RSVP_v4_{name}", col, None, 0, 0.15, alpha))
    spark_mat = make_material("Mat_RSVP_v4_Entropy_Sparks", (1,0.2,0.5,1), (1,0.2,0.5,1), 9.0)
    for i in range(spark_count):
        theta=random.random()*math.pi; ph=random.random()*2*math.pi; r=2.35+random.uniform(-.15,.35)
        loc=(r*math.sin(theta)*math.cos(ph), r*math.sin(theta)*math.sin(ph), r*math.cos(theta))
        bpy.ops.mesh.primitive_ico_sphere_add(radius=random.uniform(.06,.14), location=loc)
        s=bpy.context.active_object; s.name=f"RSVP_v4_Entropy_Spark_{i:03d}"; s.data.materials.append(spark_mat)
    bpy.ops.mesh.primitive_ico_sphere_add(radius=2.7, subdivisions=2, location=(0,0,0))
    cage=bpy.context.active_object; cage.name="RSVP_v4_Constraint_Cage"
    cage.modifiers.new("Wire", type='WIREFRAME').thickness=.035
    cage.data.materials.append(make_material("Mat_RSVP_v4_Cage", (0.6,0.8,1,1), (0.6,0.8,1,1), 4.0))

register(GeneratorSpec("rsvp_hypercell", "RSVP", "Scalar core, vector shell, coherence shell, entropy sparks, and constraint cage.", build, {"spark_count": 120}))
