from __future__ import annotations

from dataclasses import dataclass, field, asdict
from pathlib import Path
import json
import math
import random
import time
from typing import Any, Callable, Dict, Iterable, Optional

try:
    import bpy
    import mathutils
except Exception:  # Allows non-Blender test/import contexts.
    bpy = None
    mathutils = None

RGBA = tuple[float, float, float, float]

@dataclass
class RenderConfig:
    resolution_x: int = 1920
    resolution_y: int = 1080
    engine: str = "BLENDER_EEVEE"
    samples: int = 64
    film_transparent: bool = False
    frame_start: int = 1
    frame_end: int = 1
    camera_location: tuple[float, float, float] = (18.0, -18.0, 12.0)
    camera_rotation: tuple[float, float, float] = (1.2, 0.0, 0.9)
    ground_z: float = -3.0
    seed: int = 1337
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class GeneratorSpec:
    name: str
    family: str
    description: str
    builder: Callable[[RenderConfig, dict[str, Any]], None]
    defaults: dict[str, Any] = field(default_factory=dict)

REGISTRY: dict[str, GeneratorSpec] = {}

def register(spec: GeneratorSpec) -> GeneratorSpec:
    REGISTRY[spec.name] = spec
    return spec

def require_bpy() -> None:
    if bpy is None:
        raise RuntimeError("This command must be run inside Blender's Python runtime.")

def clear_scene(include_camera: bool = True, include_lights: bool = True) -> None:
    require_bpy()
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    if include_camera:
        for cam in list(bpy.data.cameras):
            bpy.data.cameras.remove(cam, do_unlink=True)
    if include_lights:
        for light in list(bpy.data.lights):
            bpy.data.lights.remove(light, do_unlink=True)

def make_material(name: str, base: RGBA=(0.8,0.8,0.8,1), emission: Optional[RGBA]=None,
                  strength: float=0.0, roughness: float=0.55, alpha: Optional[float]=None):
    require_bpy()
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        if "Base Color" in bsdf.inputs:
            bsdf.inputs["Base Color"].default_value = base
        if "Roughness" in bsdf.inputs:
            bsdf.inputs["Roughness"].default_value = roughness
        if emission and "Emission" in bsdf.inputs:
            bsdf.inputs["Emission"].default_value = emission
        if "Emission Strength" in bsdf.inputs:
            bsdf.inputs["Emission Strength"].default_value = strength
        if alpha is not None and "Alpha" in bsdf.inputs:
            bsdf.inputs["Alpha"].default_value = alpha
            mat.blend_method = 'BLEND'
            mat.use_screen_refraction = True
    return mat

def add_area_light(name: str, energy: float, loc: tuple[float, float, float], size: float=5.0):
    require_bpy()
    data = bpy.data.lights.new(name=name, type='AREA')
    data.energy = energy
    data.size = size
    obj = bpy.data.objects.new(name, data)
    obj.location = loc
    bpy.context.scene.collection.objects.link(obj)
    return obj

def setup_world(config: RenderConfig) -> None:
    require_bpy()
    scene = bpy.context.scene
    scene.render.engine = config.engine
    if hasattr(scene, "eevee"):
        scene.eevee.taa_render_samples = config.samples
    scene.render.resolution_x = config.resolution_x
    scene.render.resolution_y = config.resolution_y
    scene.render.film_transparent = config.film_transparent
    scene.frame_start = config.frame_start
    scene.frame_end = config.frame_end

    cam_data = bpy.data.cameras.new("FlyxionCam_v4")
    cam = bpy.data.objects.new("FlyxionCam_v4", cam_data)
    cam.location = config.camera_location
    cam.rotation_euler = config.camera_rotation
    bpy.context.scene.collection.objects.link(cam)
    scene.camera = cam

    add_area_light("KeyLight_v4", 3000.0, (14.0, -10.0, 16.0))
    add_area_light("FillLight_v4", 1200.0, (-12.0, -8.0, 10.0))
    add_area_light("RimLight_v4", 2200.0, (0.0, 14.0, 12.0))

    bpy.ops.mesh.primitive_plane_add(size=100.0, location=(0.0, 0.0, config.ground_z))
    ground = bpy.context.active_object
    ground.name = "GroundPlane_v4"
    ground.data.materials.append(make_material("GroundMat_v4", (0.025,0.03,0.04,1), roughness=0.97))

def vector_between(start, end):
    require_bpy()
    return mathutils.Vector(end) - mathutils.Vector(start)

def cylinder_between(start, end, radius=0.05, name="Link", material=None):
    require_bpy()
    start_v = mathutils.Vector(start)
    end_v = mathutils.Vector(end)
    direction = end_v - start_v
    length = direction.length
    if length == 0:
        return None
    mid = (start_v + end_v) / 2
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=length, location=mid)
    obj = bpy.context.active_object
    obj.name = name
    up = mathutils.Vector((0,0,1))
    obj.rotation_mode = 'QUATERNION'
    obj.rotation_quaternion = up.rotation_difference(direction.normalized())
    if material:
        obj.data.materials.append(material)
    return obj

def bezier_tube(name: str, points: list[tuple[float,float,float]], bevel_depth: float, material=None):
    require_bpy()
    curve = bpy.data.curves.new(name, 'CURVE')
    curve.dimensions = '3D'
    spline = curve.splines.new('BEZIER')
    spline.bezier_points.add(len(points)-1)
    for p, co in zip(spline.bezier_points, points):
        p.co = co
        p.handle_left_type = p.handle_right_type = 'AUTO'
    curve.bevel_depth = bevel_depth
    obj = bpy.data.objects.new(name, curve)
    bpy.context.scene.collection.objects.link(obj)
    if material:
        curve.materials.append(material)
    return obj

def write_metadata(path: Path, config: RenderConfig, generator: str, params: dict[str, Any]) -> None:
    payload = {
        "suite": "Flyxion Simulation Suite",
        "version": "4.0.0",
        "generator": generator,
        "params": params,
        "config": asdict(config),
        "unix_time": time.time(),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
