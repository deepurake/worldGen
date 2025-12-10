"""
End-to-end pipeline for 3D world generation.

This pipeline orchestrates the complete world generation process:
1. Takes a text prompt describing the desired world
2. Generates a ScenePlan using the LLM-based scene planner
3. Converts ScenePlan to 3D blockout mesh (boxes)
4. Generates a simple navmesh
"""

from scene_planner import build_scene_plan
from blockout import generate_blockout
from models import ScenePlan, BlockoutMesh, NavMesh2D

from navmesh import build_simple_navmesh


def main():
    """Main entry point for the pipeline."""
    user_prompt = "A small medieval village with a town square, houses, and a few trees"
    
    print(f"==> Building scene plan for prompt: {user_prompt!r}")
    plan = build_scene_plan(user_prompt)
    print("Scene theme:", plan.theme)
    print("Num regions:", len(plan.regions))
    print("Num objects:", len(plan.objects))
    
    print("==> Generating blockout mesh...")
    blockout = generate_blockout(plan)
    print("Blockout boxes:", len(blockout.boxes))
    
    print("==> Building simple navmesh...")
    navmesh = build_simple_navmesh(plan)
    print("Navmesh polygons:", len(navmesh.polygons))

    import json
    from dataclasses import asdict
    from reference_image import generate_reference_image

    image_out = "reference_image.png"

    print("==> Generating reference image (this may take a bit)...")
    img_path = generate_reference_image(plan, image_out)
    print("Reference image saved to:", img_path)

    # Optionally dump JSON for inspection

    with open("scene_plan.json", "w") as f:
        json.dump(asdict(plan), f, indent=2)
    print("Scene plan saved to scene_plan.json")

    with open("blockout.json", "w") as f:
        json.dump({"boxes": blockout.boxes}, f, indent=2)
    print("Blockout saved to blockout.json")

    with open("navmesh.json", "w") as f:
        json.dump({"polygons": navmesh.polygons}, f, indent=2)
    print("Navmesh saved to navmesh.json")


if __name__ == "__main__":
    main()
