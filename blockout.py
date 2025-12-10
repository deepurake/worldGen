"""
Procedural blockout generation.

Converts a ScenePlan into a BlockoutMesh (3D boxes) for visualization
and further processing.
"""

from typing import List, Tuple
from models import ScenePlan, BlockoutMesh, Vec2, Vec3

# ---------- 2) Procedural blockout ----------

GROUND_HEIGHT = 0.2
BUILDING_HEIGHT = 6.0
WALL_HEIGHT = 4.0


def box_from_region_bbox(bbox_min: Vec2, bbox_max: Vec2, height: float) -> Tuple[Vec3, Vec3]:
    (x0, y0), (x1, y1) = bbox_min, bbox_max
    cx = (x0 + x1) / 2.0
    cz = height / 2.0
    cy = (y0 + y1) / 2.0
    sx = (x1 - x0)
    sy = (y1 - y0)
    sz = height
    return (cx, cz, cy), (sx, sz, sy)


def generate_blockout(plan: ScenePlan) -> BlockoutMesh:
    boxes: List[Tuple[Vec3, Vec3]] = []

    # Ground plane
    world_w, world_h = plan.size
    ground_center: Vec3 = (world_w / 2.0, GROUND_HEIGHT / 2.0, world_h / 2.0)
    ground_size: Vec3 = (world_w, GROUND_HEIGHT, world_h)
    boxes.append((ground_center, ground_size))

    # Regions
    for r in plan.regions:
        center, size = box_from_region_bbox(r.bbox_min, r.bbox_max, GROUND_HEIGHT)
        boxes.append((center, size))

    # Objects
    for obj in plan.objects:
        x, y = obj.position
        w, d = obj.size

        if obj.kind in ("house", "tower", "building", "wall"):
            height = WALL_HEIGHT if obj.kind == "wall" else BUILDING_HEIGHT
        else:
            height = GROUND_HEIGHT * 2.0

        center: Vec3 = (x, height / 2.0, y)
        size3: Vec3 = (w, height, d)
        boxes.append((center, size3))

    return BlockoutMesh(boxes=boxes)

