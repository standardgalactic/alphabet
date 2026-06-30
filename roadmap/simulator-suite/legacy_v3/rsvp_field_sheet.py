import bpy
import math

# Clear
for obj in list(bpy.context.scene.objects):
    if obj.type in {'MESH', 'CURVE'}:
        bpy.data.objects.remove(obj, do_unlink=True)

# Simple Φ(x,y) surface as displaced grid
size = 10
step = 0.5
verts = []
faces = []
x_count = int(size/step)+1
y_count = int(size/step)+1

for iy in range(y_count):
    y = -size/2 + iy*step
    for ix in range(x_count):
        x = -size/2 + ix*step
        r = math.sqrt(x*x + y*y)
        z = 0.8*math.exp(-0.05*r*r) * math.cos(0.6*r)
        verts.append((x,y,z))

for iy in range(y_count-1):
    for ix in range(x_count-1):
        a = iy*x_count + ix
        b = a + 1
        c = a + x_count + 1
        d = a + x_count
        faces.append((a,b,c,d))

mesh = bpy.data.meshes.new("RSVP_FieldSheet")
mesh.from_pydata(verts, [], faces)
mesh.update()
obj = bpy.data.objects.new("RSVP_FieldSheet", mesh)
bpy.context.scene.collection.objects.link(obj)

m = bpy.data.materials.new("Mat_FieldSheet")
m.use_nodes = True
bsdf = m.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (0.1, 0.4, 0.8, 1.0)
bsdf.inputs["Roughness"].default_value = 0.5
obj.data.materials.append(m)

print("[v3.3] RSVP field sheet created.")
