"""
Reference image generation.

Generates a top-down concept art image from a ScenePlan using OpenAI's image generation API.
"""

import base64
from openai import OpenAI
from models import ScenePlan

client = OpenAI()

# ---------- 4) Reference image generation ----------

def generate_reference_image(plan: ScenePlan, out_path: str) -> str:
    """
    Generate a single reference image and save to disk.
    """
    # Build a compact layout description for the prompt
    region_descs = []
    for r in plan.regions:
        (x0, y0), (x1, y1) = r.bbox_min, r.bbox_max
        region_descs.append(
            f"{r.kind} '{r.name}' from ({x0:.0f},{y0:.0f}) to ({x1:.0f},{y1:.0f})"
        )

    layout_text = "; ".join(region_descs) if region_descs else "no explicit regions"

    prompt = (
        f"Top-down concept art of a {plan.theme} 3D game level, "
        f"size {plan.size[0]:.0f}x{plan.size[1]:.0f} meters. "
        f"User prompt: {plan.prompt}. "
        f"Regions layout: {layout_text}. "
        "Show clear walkable paths and coherent architecture."
    )

    img_resp = client.images.generate(
        prompt=prompt,
        n=1,
        size="1024x1024",
        response_format="b64_json",
    )

    b64_data = img_resp.data[0].b64_json
    img_bytes = base64.b64decode(b64_data)

    with open(out_path, "wb") as f:
        f.write(img_bytes)

    return out_path
