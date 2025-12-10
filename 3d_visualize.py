import trimesh
import json

data = json.load(open("blockout.json"))

scene = trimesh.Scene()

for center, size in data["boxes"]:
    cx, cy, cz = center
    sx, sy, sz = size
    box = trimesh.creation.box(extents=size)
    box.apply_translation(center)
    scene.add_geometry(box)

scene.show()
