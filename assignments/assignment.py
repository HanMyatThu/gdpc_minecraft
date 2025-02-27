from gdpc import Editor, Block
from random import randint, choice
from gdpc.geometry import placeCuboid

import numpy as np
import matplotlib.pyplot as plt

editor = Editor(buffering=False)
buildArea = editor.getBuildArea()
editor.loadWorldSlice(cache=True)

# Materials & Block Palettes for random selection
floorPalette   = [Block("quartz_block"), Block("polished_andesite"), Block("smooth_stone")]
houseWallBlock = Block("mossy_cobblestone")
grassBlock     = Block("grass_block")
lightBlock     = Block("glowstone")

print("Start building")

def get_valid_ground(x, z):
    heightmap = editor.worldSlice.heightmaps["WORLD_SURFACE"]
    local_x = x - buildArea.offset.x
    local_z = z - buildArea.offset.z
    if not (0 <= local_x < heightmap.shape[0] and 0 <= local_z < heightmap.shape[1]):
        raise IndexError(f"Coordinates ({local_x}, {local_z}) are out of bounds!")
    return heightmap[local_x, local_z] - 1

def clear_and_single_layer(x1, z1, x2, z2, base_y):
    """
    Clears everything before building a house.
    then fills exactly one layer with grass.
    """
    placeCuboid(editor, (x1, base_y, z1), (x2, base_y+20, z2), Block("air"))
    placeCuboid(editor, (x1, base_y, z1), (x2, base_y, z2), grassBlock)

def build_simple_gabled_roof(x1, z1, width, depth, base_y):
   
    stair_south = Block("spruce_stairs", {"facing": "south"})
    stair_north = Block("spruce_stairs", {"facing": "north"})
    slab_block  = Block("spruce_slab",   {"type": "bottom"})
    
    half_depth = (depth + 1) // 2
    for i in range(half_depth):
        front_z = z1 + i
        back_z  = z1 + (depth - 1 - i)
        roof_y  = base_y + i
        
        for x in range(x1, x1 + width):
            editor.placeBlock((x, roof_y, front_z), stair_south)
        
        if back_z > front_z:
            for x in range(x1, x1 + width):
                editor.placeBlock((x, roof_y, back_z), stair_north)

    if depth % 2 == 1:
        center_z = z1 + depth // 2
        center_y = base_y + depth // 2
        for x in range(x1, x1 + width):
            editor.placeBlock((x, center_y, center_z), slab_block)


# Get base position
heightmap = editor.worldSlice.heightmaps["WORLD_SURFACE"]
max_x = buildArea.offset.x + heightmap.shape[0] - 1
max_z = buildArea.offset.z + heightmap.shape[1] - 1

# Choose a random valid coordinate for the house
x0 = randint(buildArea.offset.x, max_x)
z0 = randint(buildArea.offset.z, max_z)
y0 = get_valid_ground(x0, z0)

# House dimensions, random values
house_margin = 6
width  = randint(14, 16)
depth  = randint(12, 14)
groundHeight = 4

prop_min_x = x0 - house_margin
prop_max_x = x0 + width + house_margin
prop_min_z = z0 - house_margin
prop_max_z = z0 + depth + house_margin
clear_and_single_layer(prop_min_x, prop_min_z, prop_max_x, prop_max_z, y0)

# Random floor block
floorBlock = choice(floorPalette)

# House Floor
placeCuboid(editor, (x0, y0, z0), (x0+width, y0+1, z0+depth), floorBlock)

placeCuboid(editor, (x0+1, y0+1, z0+1),
            (x0+width-1, y0+groundHeight, z0+depth-1),
            Block("air"))

# --- Building Walls ---
placeCuboid(editor, (x0, y0, z0),
            (x0+width, y0+groundHeight, z0+1),
            houseWallBlock)
placeCuboid(editor, (x0, y0, z0+depth-1),
            (x0+width, y0+groundHeight, z0+depth),
            houseWallBlock)
placeCuboid(editor, (x0, y0, z0),
            (x0+1, y0+groundHeight, z0+depth),
            houseWallBlock)
placeCuboid(editor, (x0+width-1, y0, z0),
            (x0+width, y0+groundHeight, z0+depth),
            houseWallBlock)

placeCuboid(editor, (x0, y0+groundHeight, z0),
            (x0+width, y0+groundHeight+1, z0+depth),
            houseWallBlock)

# --- Front Door ---
door_x_left  = x0 + width//2 - 1
door_x_right = door_x_left + 1

placeCuboid(editor, (door_x_left, y0, z0),
            (door_x_right+1, y0+1, z0+1),
            floorBlock)
placeCuboid(editor, (door_x_left, y0+1, z0),
            (door_x_right+1, y0+3, z0+1),
            Block("air"))

# Place double doors
editor.placeBlock((door_x_left,  y0+1, z0), Block("oak_door", {"half": "lower", "facing": "south"}))
editor.placeBlock((door_x_left,  y0+2, z0), Block("oak_door", {"half": "upper", "facing": "south"}))
editor.placeBlock((door_x_right, y0+1, z0), Block("oak_door", {"half": "lower", "facing": "south"}))
editor.placeBlock((door_x_right, y0+2, z0), Block("oak_door", {"half": "upper", "facing": "south"}))
editor.placeBlock((door_x_right + 1, y0+1, z0), Block("oak_door", {"half": "lower", "facing": "south"}))
editor.placeBlock((door_x_right + 1, y0+2, z0), Block("oak_door", {"half": "upper", "facing": "south"}))

# --- Interior Decorations ---
living_x = x0 + 2
living_z = z0 + 3
editor.placeBlock((living_x,     y0+1, living_z), Block("dark_oak_stairs", {"facing": "east"}))
editor.placeBlock((living_x + 1, y0+1, living_z), Block("dark_oak_stairs", {"facing": "east"}))

# Couch
editor.placeBlock((living_x,     y0+2, living_z), Block("red_wool"))
editor.placeBlock((living_x + 1, y0+2, living_z), Block("red_wool"))

# TV 
tv_x = living_x + 4
editor.placeBlock((tv_x, y0+1, living_z), Block("black_concrete"))

# Dining Table
dining_x = x0 + width//2 - 2
dining_z = z0 + depth//2 - 1
placeCuboid(editor, (dining_x, y0+1, dining_z),
            (dining_x+3, y0+1, dining_z+1),
            Block("oak_slab"))

# Chairs
editor.placeBlock((dining_x,     y0+1, dining_z+1), Block("oak_stairs", {"facing": "east"}))
editor.placeBlock((dining_x + 3, y0+1, dining_z+1), Block("oak_stairs", {"facing": "west"}))

# Kitchen
kitchen_x = x0 + width - 5
kitchen_z = z0 + depth - 5
editor.placeBlock((kitchen_x,     y0+1, kitchen_z), Block("crafting_table"))
editor.placeBlock((kitchen_x + 1, y0+1, kitchen_z), Block("furnace"))
editor.placeBlock((kitchen_x + 2, y0+1, kitchen_z), Block("smoker"))
editor.placeBlock((kitchen_x + 3, y0+1, kitchen_z), Block("barrel"))

# Table in front of the kitchen
table_x = kitchen_x - 4
table_z = kitchen_z
placeCuboid(editor, (table_x, y0+1, table_z),
            (table_x+1, y0+1, table_z+1),
            Block("oak_slab"))
editor.placeBlock((table_x,   y0+1, table_z+2), Block("oak_stairs", {"facing": "south"}))
editor.placeBlock((table_x+1, y0+1, table_z+2), Block("oak_stairs", {"facing": "south"}))

# Bedroom
bed_x = x0 + 4
bed_z = z0 + depth - 4
editor.placeBlock((bed_x, y0+1, bed_z), Block("orange_bed", {"facing": "south"}))

# --- Ceiling Lights ---
ceiling_y = y0 + groundHeight - 1
light_positions = [
    (x0 + width//3, ceiling_y, z0 + depth//2),
    (x0 + width//2, ceiling_y, z0 + depth//2),
    (x0 + 2*width//3, ceiling_y, z0 + depth//2),
]
for lx, ly, lz in light_positions:
    editor.placeBlock((lx, ly, lz), lightBlock)

# -----------------------------------------------------------
#                   Building Roof
# -----------------------------------------------------------
roof_base_y = y0 + groundHeight + 1
build_simple_gabled_roof(
    x1=x0,
    z1=z0 + 1,
    width=width,
    depth=depth,
    base_y=roof_base_y
)

# -----------------------------------------------------------
#                   Building Fence Walls
# -----------------------------------------------------------
fence_y = y0 + 1
for x in range(prop_min_x, prop_max_x):
    # South & North edges
    editor.placeBlock((x, fence_y, prop_min_z), Block("oak_fence"))
    editor.placeBlock((x, fence_y, prop_max_z - 1), Block("oak_fence"))
    editor.placeBlock((x, fence_y - 1, prop_min_z), Block("oak_fence"))
    editor.placeBlock((x, fence_y - 1 , prop_max_z - 1), Block("oak_fence"))
for z in range(prop_min_z, prop_max_z):
    # West & East edges
    editor.placeBlock((prop_min_x, fence_y, z), Block("oak_fence"))
    editor.placeBlock((prop_max_x - 1, fence_y, z), Block("oak_fence"))
    editor.placeBlock((prop_min_x, fence_y - 1, z), Block("oak_fence"))
    editor.placeBlock((prop_max_x - 1, fence_y - 1, z), Block("oak_fence"))

# 2-wide entrance on the south fence
entrance_left  = (prop_min_x + prop_max_x)//2 - 1
entrance_right = entrance_left + 1
editor.placeBlock((entrance_left,  fence_y, prop_min_z), Block("air"))
editor.placeBlock((entrance_right, fence_y, prop_min_z), Block("air"))
editor.placeBlock((entrance_left,  fence_y, prop_min_z), Block("oak_fence_gate", {"facing": "south"}))
editor.placeBlock((entrance_right, fence_y, prop_min_z), Block("oak_fence_gate", {"facing": "south"}))

# -----------------------------------------------------------
#  Extended Walking Path 
# -----------------------------------------------------------
# Skip placing the fence line on the path area,

path_min_z = prop_min_z - 5  
path_max_z = z0 - 1          

if path_min_z < path_max_z:
    cobble = Block("cobblestone")

    if path_min_z < prop_min_z:
        z_end = min(prop_min_z - 1, path_max_z)
        if path_min_z <= z_end:
            placeCuboid(editor,
                        (entrance_left,  y0, path_min_z),
                        (entrance_right, y0, z_end),
                        cobble)

    if prop_min_z + 1 <= path_max_z:
        placeCuboid(editor,
                    (entrance_left,  y0, prop_min_z + 1),
                    (entrance_right, y0, path_max_z),
                    cobble)

# -----------------------------------------------------------
#   Tall Plant
# -----------------------------------------------------------
plant_base_x = x0 + width + 2
plant_base_z = z0 + 2
if plant_base_x >= prop_max_x - 1:
    plant_base_x = prop_max_x - 2
if plant_base_z >= prop_max_z - 1:
    plant_base_z = prop_max_z - 2

# Trunk
for i in range(5):
    editor.placeBlock((plant_base_x, y0+1+i, plant_base_z), Block("stripped_spruce_log"))
# Leaves at the top
for dx in [-1, 0, 1]:
    for dz in [-1, 0, 1]:
        editor.placeBlock((plant_base_x + dx, y0+6, plant_base_z + dz), Block("oak_leaves"))

# -----------------------------------------------------------
#                          GARDEN
# -----------------------------------------------------------
garden_x1 = x0 - 5
garden_x2 = x0 - 1
garden_z1 = z0 + 2
garden_z2 = z0 + depth - 2
if garden_x1 < prop_min_x:
    garden_x1 = prop_min_x
if garden_x2 > prop_max_x - 1:
    garden_x2 = prop_max_x - 1
if garden_z2 > prop_max_z - 1:
    garden_z2 = prop_max_z - 1

placeCuboid(editor, (garden_x1, y0+1, garden_z1), (garden_x2, y0+2, garden_z2), Block("air"))
flowers = [Block("poppy"), Block("dandelion"), Block("blue_orchid"), Block("flower_pot")]
for gx in range(garden_x1, garden_x2):
    for gz in range(garden_z1, garden_z2):
        if randint(0, 4) == 0:
            editor.placeBlock((gx, y0, gz), choice(flowers))

print("House built successfully!")

# heatmap for the house and terrain
heightmap = editor.worldSlice.heightmaps["WORLD_SURFACE"]
terrain_array = np.array(heightmap)

plt.figure(figsize=(10, 6))
plt.imshow(terrain_array, cmap="terrain", origin="lower")
plt.scatter(x0, z0, color="red", marker="x", s=100, label="House Placement")
plt.colorbar(label="Elevation (Blocks)")
plt.title("Minecraft Terrain with House Placement")
plt.xlabel("X Coordinate")
plt.ylabel("Z Coordinate")
plt.legend()
plt.show()
