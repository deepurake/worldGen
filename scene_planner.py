import os
import json
import base64
from dataclasses import dataclass, field, asdict
from typing import List, Tuple, Dict, Any

from openai import OpenAI
from models import ScenePlan, Region, SceneObject

client = OpenAI()

# ---------- 1) LLM: prompt -> ScenePlan ----------
SCENE_PLANNER_SYSTEM_PROMPT = """
You are a level designer AI.

Given a short text prompt describing a 3D world, you MUST output a JSON object
describing a 50x50 meter game level.

The JSON MUST have the following structure:

{
  "theme": "string",
  "size": [50, 50],
  "regions": [
    {
      "id": "region_1",
      "name": "Town Square",
      "kind": "plaza",
      "bbox_min": [5, 5],
      "bbox_max": [20, 20]
    }
  ],
  "objects": [
    {
      "id": "obj_1",
      "kind": "house",
      "region_id": "region_1",
      "position": [10, 10],
      "size": [4, 4],
      "rotation": 0.0
    }
  ],
  "notes": {
    "lighting": "warm, evening",
    "weather": "clear"
  }
}

Constraints:
- Coordinates are in meters, x and y between 0 and 50.
- Define 2-6 regions.
- Define 10-40 objects.
- Layout should be coherent and walkable.
- DO NOT output anything except valid JSON.
"""

def call_llm_for_plan(user_prompt: str) -> Dict[str, Any]:
    """Call OpenAI API and get JSON back."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SCENE_PLANNER_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Prompt: {user_prompt}\n\nReturn ONLY JSON."
            },
        ],
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content
    return json.loads(content)


def build_scene_plan(user_prompt: str) -> ScenePlan:
    raw = call_llm_for_plan(user_prompt)

    regions = [
        Region(
            id=r["id"],
            name=r["name"],
            kind=r["kind"],
            bbox_min=tuple(r["bbox_min"]),
            bbox_max=tuple(r["bbox_max"]),
        )
        for r in raw.get("regions", [])
    ]

    objects = [
        SceneObject(
            id=o["id"],
            kind=o["kind"],
            region_id=o["region_id"],
            position=tuple(o["position"]),
            size=tuple(o["size"]),
            rotation=float(o.get("rotation", 0.0)),
        )
        for o in raw.get("objects", [])
    ]

    size = raw.get("size", [50.0, 50.0])

    return ScenePlan(
        prompt=user_prompt,
        theme=raw.get("theme", "unknown"),
        size=(float(size[0]), float(size[1])),
        regions=regions,
        objects=objects,
        notes=raw.get("notes", {}),
    )