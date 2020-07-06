from PIL import Image
import numpy as numpy
import os

biomes = [
        {"id": 12, "name": "Snowy Tundra"},
        {"id": 0, "name": "Ocean"},
        {"id": 1, "name": "Plains"},
        {"id": 2, "name": "Desert"},
        {"id": 3, "name": "Mountains"},
        {"id": 4, "name": "Forest"},
        {"id": 5, "name": "Taiga"},
        {"id": 6, "name": "Swamp"},
        {"id": 7, "name": "River"},
        {"id": 8, "name": "Nether Wastes"},
        {"id": 9, "name": "The End"},
        {"id": 10, "name": "Frozen Ocean"},
        {"id": 11, "name": "Frozen River"},
        {"id": 13, "name": "Snowy Mountains"},
        {"id": 14, "name": "Mushroom Fields"},
        {"id": 15, "name": "Mushroom Fields Shore"},
        {"id": 16, "name": "Beach"},
        {"id": 17, "name": "Desert Hills"},
        {"id": 18, "name": "Wooded Hills"},
        {"id": 19, "name": "Taiga Hills"},
        {"id": 20, "name": "Mountain Edge"},
        {"id": 21, "name": "Jungle"},
        {"id": 22, "name": "Jungle Hills"},
        {"id": 23, "name": "Jungle Edge"},
        {"id": 24, "name": "Deep Ocean"},
        {"id": 25, "name": "Stone Shore"},
        {"id": 26, "name": "Snowy Beach"},
        {"id": 27, "name": "Birch Forest"},
        {"id": 28, "name": "Birch Forest Hills"},
        {"id": 29, "name": "Dark Forest"},
        {"id": 30, "name": "Snowy Taiga"},
        {"id": 31, "name": "Snowy Taiga Hills"},
        {"id": 32, "name": "Giant Tree Taiga"},
        {"id": 33, "name": "Giant Tree Taiga Hills"},
        {"id": 34, "name": "Wooded Mountains"},
        {"id": 35, "name": "Savanna"},
        {"id": 36, "name": "Savanna Plateau"},
        {"id": 37, "name": "Badlands"},
        {"id": 38, "name": "Wooded Badlands Plateau"},
        {"id": 39, "name": "Badlands Platuea"},
        {"id": 40, "name": "Small End Islands"},
        {"id": 41, "name": "End Midlands"},
        {"id": 42, "name": "End Highlands"},
        {"id": 43, "name": "End Barrens"},
        {"id": 44, "name": "Warm Ocean"},
        {"id": 45, "name": "Lukewarm Ocean"},
        {"id": 46, "name": "Cold Ocean"},
        {"id": 47, "name": "Deep Warm Ocean"},
        {"id": 48, "name": "Deep Lukewarm Ocean"},
        {"id": 49, "name": "Deep Cold Ocean"},
        {"id": 50, "name": "Deep Frozen Ocean"},
        {"id": 127, "name": "The Void"},
        {"id": 129, "name": "Sunflower Plains"},
        {"id": 130, "name": "Desert Lakes"},
        {"id": 131, "name": "Gravelly Mountains"},
        {"id": 132, "name": "Flower Forest"},
        {"id": 133, "name": "Taiga Mountains"},
        {"id": 134, "name": "Swamp Hills"},
        {"id": 140, "name": "Ice Spikes"},
        {"id": 149, "name": "Modified Jungle"},
        {"id": 151, "name": "Modified Jungle Edge"},
        {"id": 155, "name": "Tall Birch Forest"},
        {"id": 156, "name": "Tall Birch Hills"},
        {"id": 157, "name": "Dark Forest Hills"},
        {"id": 158, "name": "Snowy Taiga Mountains"},
        {"id": 160, "name": "Giant Spruce Taiga"},
        {"id": 161, "name": "Giant Spruce Taiga Hills"},
        {"id": 162, "name": "Gravelly Mountains+"},
        {"id": 163, "name": "Shattered Savanna"},
        {"id": 164, "name": "Shattered Savanna Plateau"},
        {"id": 165, "name": "Eroded Badlands"},
        {"id": 166, "name": "Modified Wooded Badlands Plateau"},
        {"id": 167, "name": "Modified Badlands Plateau"},
        {"id": 168, "name": "Bamboo Jungle"},
        {"id": 169, "name": "Bamboo Jungle Hills"},
        {"id": 170, "name": "Soul Sand Valley"},
        {"id": 171, "name": "Crimson Forest"},
        {"id": 172, "name": "Warped Forest"},
        {"id": 173, "name": "Basalt Deltas"},
        ]

#
# Function obtained from Martin Thoma on stackoverflow:
# https://stackoverflow.com/questions/138250/how-to-read-the-rgb-value-of-a-given-pixel-in-python
#
def get_image(image_path):
    """Get a numpy array of an image so that one can access values[x][y]."""
    image = Image.open(image_path, 'r')
    width, height = image.size
    pixel_values = list(image.getdata())
    if image.mode == 'RGBA':
        channels = 4
    elif image.mode == 'RGB':
        channels = 3
    elif image.mode == 'L':
        channels = 1
    else:
        print("Unknown mode: %s" % image.mode)
        return None
    pixel_values = numpy.array(pixel_values).reshape((height, width, channels))
    return image, pixel_values

#
# Create a dictionary that maps colours to biome id and name
# colour follows from https://github.com/toolbox4minecraft/amidst/wiki/Biome-Color-Table
# Note: end biomes have different colours between the github page and the colours that chunkbase used
#
col_to_biomes = dict()   # "(RRR, GGG, BBB, 255)": {id, name}

for i in range(1,3):
    im, arr = get_image(f"data/colours{i}.png")
    arr = arr[:, 50]
    for pixel in arr:
        # turn into a string so that a pixel is hashable (a list is not hashable, but a string is)
        pix_str = f"({pixel[0]}, {pixel[1]}, {pixel[2]}, 255)"
        
        # don't include dark bg, light bg, gridline; only include unique entries
        if pix_str not in ["(246, 248, 250, 255)", "(223, 226, 229, 255)"] and pix_str not in col_to_biomes.keys():
            col_to_biomes[pix_str] = biomes[len(col_to_biomes)]



#
# Read all the downloaded maps and calculate the biome coverage
#
            
# Initialize biome counts to 0. Format: {id: count}
biome_counts = {biome_dict["id"]: 0 for biome_dict in biomes}
biome_counts[-1] = 0   # Explicitly include unidentified biome id

maps_path = "data/overworld/"
world_data = os.listdir(maps_path)
for world_img in world_data:
    im = Image.open(maps_path + world_img, "r")
    w, h = im.size
    bounding_box = (87, 54, w-23, h-44)
    
    im = im.crop(bounding_box)
    for pixel in list(im.getdata()):
        biome_id = col_to_biomes.get(str(pixel), {"id": -1}).get("id")
    #    if biome_id == -1:
    #        print(str(pixel) + " at (" + str(counter//w) + ", " + str(counter%w) + ")")
        biome_counts[biome_id] += 1   # biome_counts is initialized, so we don't need to further enxure the id is in the dict

# Remove unidentified biomes (which shouldn't happen...)
print("Unidentified chunks:", biome_counts.pop(-1) if biome_counts.get(-1, None) is not None else None)

print("Raw number of chunks:")
pprint.pprint(biome_counts)

# Calculate the percentage
total = sum([num_chunks for num_chunks in biome_counts.values()])
print("Chunks identified:", total)
for (bid, count) in biome_counts.items():
    biome_counts[bid] = count / total
    
print("Percentage Coverage:")
pprint.pprint(biome_counts)
    