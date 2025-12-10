from dataclasses import dataclass, field
from typing import List, Dict, Tuple

# Type aliases for clarity
Vec2 = Tuple[float, float]
Vec3 = Tuple[float, float, float]


@dataclass
class SceneObject:
    id: str
    kind: str          # "house", "tree", "road", etc.
    region_id: str
    position: Vec2     # (x, y)
    size: Vec2         # footprint (width, depth)
    rotation: float    # degrees


@dataclass
class Region:
    id: str
    name: str
    kind: str          # "plaza", "residential", etc.
    bbox_min: Vec2
    bbox_max: Vec2


@dataclass
class ScenePlan:
    prompt: str
    theme: str
    size: Vec2                       # (width, height) in meters
    regions: List[Region] = field(default_factory=list)
    objects: List[SceneObject] = field(default_factory=list)
    notes: Dict[str, str] = field(default_factory=dict)


@dataclass
class BlockoutMesh:
    # Each box: (center, size)
    boxes: List[Tuple[Vec3, Vec3]]   # ((cx, cy, cz), (sx, sy, sz))


@dataclass
class NavMesh2D:
    # List of polygons, each a list of (x, y)
    polygons: List[List[Vec2]]

