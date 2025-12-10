import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Load JSONs
plan = json.load(open("scene_plan.json"))
blockout = json.load(open("blockout.json"))
navmesh = json.load(open("navmesh.json"))

fig, ax = plt.subplots(figsize=(8, 8))

# --- Draw regions ---
for r in plan["regions"]:
    (x0, y0) = r["bbox_min"]
    (x1, y1) = r["bbox_max"]

    rect = patches.Rectangle(
        (x0, y0),
        x1 - x0,
        y1 - y0,
        linewidth=2,
        edgecolor="blue",
        facecolor="none"
    )
    ax.add_patch(rect)
    ax.text(x0, y0, r["name"], color="blue")

# --- Draw objects ---
for obj in plan["objects"]:
    (x, y) = obj["position"]
    (w, h) = obj["size"]

    rect = patches.Rectangle(
        (x - w/2, y - h/2),
        w,
        h,
        linewidth=1,
        edgecolor="green",
        facecolor="none"
    )
    ax.add_patch(rect)

# --- Draw navmesh polygons ---
for poly in navmesh["polygons"]:
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    ax.plot(xs + [xs[0]], ys + [ys[0]], color="orange")

ax.set_xlim(0, plan["size"][0])
ax.set_ylim(0, plan["size"][1])
ax.set_aspect("equal")
ax.set_title("Scene Plan Visualization")
plt.show()
