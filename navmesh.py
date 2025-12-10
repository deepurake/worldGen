"""
Simple navmesh generation.

Converts a ScenePlan into a NavMesh2D for pathfinding.
"""

import math
from shapely.geometry import Polygon, Point
from shapely.ops import unary_union

from models import ScenePlan, NavMesh2D, Vec2


def create_obstacle_polygon(obj) -> Polygon:
    """
    Create a polygon representing an obstacle's footprint.
    
    Objects are positioned at their center, so we create a rectangle
    centered at the position, accounting for rotation.
    """
    x, y = obj.position
    w, h = obj.size
    
    # Half dimensions
    hw = w / 2.0
    hh = h / 2.0
    
    # Create rectangle corners in local space (centered at origin)
    corners = [
        (-hw, -hh),
        (hw, -hh),
        (hw, hh),
        (-hw, hh),
    ]
    
    # Apply rotation
    if obj.rotation != 0.0:
        rad = math.radians(obj.rotation)
        cos_r = math.cos(rad)
        sin_r = math.sin(rad)
        rotated_corners = []
        for cx, cy in corners:
            rx = cx * cos_r - cy * sin_r
            ry = cx * sin_r + cy * cos_r
            rotated_corners.append((rx, ry))
        corners = rotated_corners
    
    # Translate to world position
    world_corners = [(x + cx, y + cy) for cx, cy in corners]
    
    return Polygon(world_corners)


def build_simple_navmesh(plan: ScenePlan) -> NavMesh2D:
    """
    Build a simple 2D navmesh from a scene plan.
    
    Creates walkable areas by subtracting obstacles from the world bounds.
    Only objects that are obstacles (houses, buildings, walls, etc.) are excluded.
    """
    world_w, world_h = plan.size
    
    # Create world bounds polygon
    world_polygon = Polygon([
        (0.0, 0.0),
        (world_w, 0.0),
        (world_w, world_h),
        (0.0, world_h),
    ])
    
    # Filter objects that are obstacles (non-walkable)
    # Typically buildings, walls, and structures are obstacles
    # Trees and decorative objects might be walkable, but for simplicity,
    # we'll treat houses, buildings, towers, and walls as obstacles
    obstacle_kinds = {"house", "building", "tower", "wall", "structure"}
    
    obstacle_polygons = []
    for obj in plan.objects:
        if obj.kind.lower() in obstacle_kinds:
            try:
                obstacle_poly = create_obstacle_polygon(obj)
                if obstacle_poly.is_valid:
                    obstacle_polygons.append(obstacle_poly)
            except Exception:
                # Skip invalid polygons
                continue
    
    # Subtract obstacles from world polygon
    if obstacle_polygons:
        # Combine all obstacles into a single polygon
        obstacles_union = unary_union(obstacle_polygons)
        
        # Subtract obstacles from world
        walkable_area = world_polygon.difference(obstacles_union)
        
        # Convert result to list of polygons
        # If the result is a MultiPolygon, extract individual polygons
        if hasattr(walkable_area, 'geoms'):
            polygons = []
            for geom in walkable_area.geoms:
                if isinstance(geom, Polygon) and geom.is_valid:
                    coords = list(geom.exterior.coords)
                    # Remove duplicate last point (shapely closes the polygon)
                    if len(coords) > 1 and coords[0] == coords[-1]:
                        coords = coords[:-1]
                    polygons.append(coords)
        else:
            # Single polygon result
            if isinstance(walkable_area, Polygon) and walkable_area.is_valid:
                coords = list(walkable_area.exterior.coords)
                if len(coords) > 1 and coords[0] == coords[-1]:
                    coords = coords[:-1]
                polygons = [coords]
            else:
                # Fallback to world polygon if something went wrong
                polygons = [[(0.0, 0.0), (world_w, 0.0), (world_w, world_h), (0.0, world_h)]]
    else:
        # No obstacles, return world polygon
        polygons = [[(0.0, 0.0), (world_w, 0.0), (world_w, world_h), (0.0, world_h)]]
    
    return NavMesh2D(polygons=polygons)

