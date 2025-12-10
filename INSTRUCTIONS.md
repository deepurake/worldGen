# WorldGen - Setup and Usage Instructions

This document provides step-by-step instructions for setting up and using the WorldGen 3D world generation system.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Usage](#usage)
5. [Project Structure](#project-structure)
6. [Individual Components](#individual-components)
7. [Output Files](#output-files)
8. [Troubleshooting](#troubleshooting)

## Prerequisites

- **Python 3.8+** (Python 3.9 or higher recommended)
- **OpenAI API Key** - Required for LLM-based scene planning and image generation
- **pip** - Python package manager

## Installation

### 1. Clone or Navigate to the Project Directory

```bash
cd /path/to/worldGen
```

### 2. Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `openai` - OpenAI API client for LLM and image generation
- `matplotlib` - Visualization library
- `trimesh` - 3D mesh processing
- `pyglet` - 3D visualization (version < 2)
- `shapely` - 2D polygon operations for navmesh generation

## Configuration

### OpenAI API Key Setup

The project requires an OpenAI API key for:
- Scene planning (using GPT-4o-mini)
- Reference image generation (using DALL-E)

**Option 1: Environment Variable (Recommended)**

```bash
# On macOS/Linux:
export OPENAI_API_KEY="your-api-key-here"

# On Windows:
set OPENAI_API_KEY=your-api-key-here
```

**Option 2: Create a `.env` file**

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your-api-key-here
```

Note: The `.env` file is already in `.gitignore` to prevent committing secrets.

**Getting an API Key:**
1. Sign up at [OpenAI Platform](https://platform.openai.com/)
2. Navigate to API Keys section
3. Create a new secret key
4. Copy and use it as shown above

## Usage

### Running the Full Pipeline

The main pipeline generates a complete 3D world from a text prompt:

```bash
python pipeline.py
```

This will:
1. Generate a scene plan using the LLM
2. Create a 3D blockout mesh
3. Generate a navmesh for pathfinding
4. Create a reference image
5. Save all outputs to JSON files

**Default Prompt:** "A small medieval village with a town square, houses, and a few trees"

**To customize the prompt**, edit `pipeline.py` and modify the `user_prompt` variable in the `main()` function.

### Running Individual Components

#### 1. Scene Planning Only

```python
from scene_planner import build_scene_plan

plan = build_scene_plan("Your custom prompt here")
print(f"Theme: {plan.theme}")
print(f"Regions: {len(plan.regions)}")
print(f"Objects: {len(plan.objects)}")
```

#### 2. Generate Blockout Mesh

```python
from scene_planner import build_scene_plan
from blockout import generate_blockout

plan = build_scene_plan("Your prompt")
blockout = generate_blockout(plan)
print(f"Generated {len(blockout.boxes)} boxes")
```

#### 3. Generate Navmesh

```python
from scene_planner import build_scene_plan
from navmesh import build_simple_navmesh

plan = build_scene_plan("Your prompt")
navmesh = build_simple_navmesh(plan)
print(f"Generated {len(navmesh.polygons)} walkable polygons")
```

#### 4. Generate Reference Image

```python
from scene_planner import build_scene_plan
from reference_image import generate_reference_image

plan = build_scene_plan("Your prompt")
image_path = generate_reference_image(plan, "output_image.png")
print(f"Image saved to: {image_path}")
```

#### 5. Visualize Scene Plan

```bash
python visualize_plan.py
```

This requires existing JSON files (`scene_plan.json`, `blockout.json`, `navmesh.json`) and displays a 2D visualization using matplotlib.

#### 6. 3D Visualization

```bash
python 3d_visualize.py
```

Opens a 3D interactive visualization of the blockout mesh using pyglet.

## Project Structure

```
worldGen/
├── pipeline.py              # Main end-to-end pipeline
├── scene_planner.py          # LLM-based scene planning
├── blockout.py               # 3D blockout mesh generation
├── navmesh.py                # Navmesh generation for pathfinding
├── reference_image.py        # Reference image generation
├── models.py                 # Data models (ScenePlan, NavMesh2D, etc.)
├── visualize_plan.py         # 2D visualization
├── 3d_visualize.py          # 3D visualization
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore rules
├── README.md                # Project overview
└── INSTRUCTIONS.md          # This file
```

## Individual Components

### Scene Planner (`scene_planner.py`)

- **Purpose:** Converts text prompts into structured scene plans
- **Input:** Text description of desired world
- **Output:** `ScenePlan` object with regions, objects, and metadata
- **Model:** GPT-4o-mini (via OpenAI API)

### Blockout Generator (`blockout.py`)

- **Purpose:** Converts scene plans into 3D blockout meshes
- **Input:** `ScenePlan` object
- **Output:** `BlockoutMesh` with 3D boxes
- **Features:** Creates ground plane, region boxes, and object boxes with appropriate heights

### Navmesh Generator (`navmesh.py`)

- **Purpose:** Creates walkable areas for pathfinding
- **Input:** `ScenePlan` object
- **Output:** `NavMesh2D` with walkable polygons
- **Features:** 
  - Subtracts obstacles (houses, buildings, walls) from world bounds
  - Handles rotated objects
  - Creates multiple walkable regions if obstacles split the world

### Reference Image Generator (`reference_image.py`)

- **Purpose:** Generates top-down concept art from scene plans
- **Input:** `ScenePlan` object and output path
- **Output:** PNG image file
- **Model:** DALL-E (via OpenAI API)

## Output Files

After running the pipeline, the following files are generated:

- **`scene_plan.json`** - Complete scene plan with regions and objects
- **`blockout.json`** - 3D blockout mesh data (boxes)
- **`navmesh.json`** - 2D navmesh polygons for pathfinding
- **`reference_image.png`** - Top-down reference image

**Note:** These files are in `.gitignore` and won't be committed to version control.

## Troubleshooting

### Common Issues

#### 1. OpenAI API Key Not Found

**Error:** `AuthenticationError` or `API key not found`

**Solution:**
- Ensure `OPENAI_API_KEY` environment variable is set
- Verify the API key is correct and has credits
- Check that the virtual environment is activated

#### 2. Import Errors

**Error:** `ModuleNotFoundError`

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### 3. Shapely Installation Issues

**Error:** `Failed to build shapely`

**Solution:**
```bash
# Install system dependencies first (macOS)
brew install geos

# Or use conda
conda install -c conda-forge shapely

# Then install requirements
pip install -r requirements.txt
```

#### 4. Invalid Polygon Errors in Navmesh

**Error:** `TopologyException` or invalid geometry warnings

**Solution:**
- This can occur with overlapping or invalid obstacle polygons
- The code includes error handling to skip invalid obstacles
- Check that object positions and sizes are reasonable

#### 5. Image Generation Fails

**Error:** `RateLimitError` or timeout

**Solution:**
- Check OpenAI API rate limits
- Ensure you have sufficient API credits
- Wait and retry if rate limited

### Getting Help

- Check the error message for specific details
- Verify all dependencies are installed correctly
- Ensure API keys are properly configured
- Review the generated JSON files to debug scene planning issues

## Advanced Usage

### Customizing Scene Plans

Edit `scene_planner.py` to modify:
- System prompt for scene planning
- Model selection (currently GPT-4o-mini)
- Response format and constraints

### Customizing Blockout Generation

Edit `blockout.py` to modify:
- Height constants (`GROUND_HEIGHT`, `BUILDING_HEIGHT`, `WALL_HEIGHT`)
- Object type classifications
- Box generation logic

### Customizing Navmesh Generation

Edit `navmesh.py` to modify:
- Obstacle type filtering (which objects block navigation)
- Polygon simplification
- Walkable area generation algorithms

## Next Steps

- Experiment with different prompts to generate various world types
- Visualize outputs using the provided visualization scripts
- Integrate generated data into game engines or 3D applications
- Extend the system with additional features (terrain generation, object placement algorithms, etc.)

---

**Happy World Building!** 🌍

