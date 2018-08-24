import yaml
from PIL import Image
import math
from tools import get_files_names

PATH = 'maps'

def find_bounds(map_image):
    x_min = map_image.size[0]
    x_end = 0
    y_min = map_image.size[1]
    y_end = 0
    pix = map_image.load()
    for x in range(map_image.size[0]):
        for y in range(map_image.size[1]):
            val = pix[x, y]
            if val != 205 and val != 128:  # not unknown
                x_min = min(x, x_min)
                x_end = max(x, x_end)
                y_min = min(y, y_min)
                y_end = max(y, y_end)
    return x_min, x_end, y_min, y_end


def computed_cropped_origin(map_image, bounds, resolution, origin):
    """ Compute the image for the cropped map when map_image is cropped by bounds and had origin before. """
    ox = origin[0]
    oy = origin[1]
    oth = origin[2]

    # First figure out the delta we have to translate from the lower left corner (which is the origin)
    # in the image system
    dx = bounds[0] * resolution
    dy = (map_image.size[1] - bounds[3]) * resolution

    # Next rotate this by the theta and add to the old origin
    new_ox = ox + dx * math.cos(oth) - dy * math.sin(oth)
    new_oy = oy + dx * math.sin(oth) + dy * math.cos(oth)

    return [new_ox, new_oy, oth]


def crop_map(filename, path = ""):
    """" Process to crop of the image indicate in filename """

    if path!= "":
        path += "/"

    crop_name = '.'.join(filename.split(".")[:-1])

    with open(path + str(crop_name) + ".yaml") as f:
        map_data = yaml.safe_load(f)

    crop_yaml = crop_name + ".yaml"
    map_image_file = str(map_data["image"])

    resolution = map_data["resolution"]
    origin = map_data["origin"]

    print("Openning " + path + map_image_file)
    map_image = Image.open(path + map_image_file)
    width, height = map_image.size
    bounds = find_bounds(map_image)
    if bounds[0] == 0 and width == (bounds[1] + 1) and bounds[2] == 0 and height == (bounds[3] + 1):
        print("No need to crop " + str(crop_name))

    else:
        print("Cropping " + str(crop_name))
        # left, upper, right, lower
        cropped_image = map_image.crop((bounds[0], bounds[2], bounds[1] + 1, bounds[3] + 1))
        cropped_image.save(path + map_image_file)
        map_data["image"] = map_image_file
        map_data["origin"] = computed_cropped_origin(map_image, bounds, resolution, origin)
        with open(path + "/" + crop_yaml, "w") as f:
            yaml.dump(map_data, f)
            print("End of cropping")


def main():
    for mapName in get_files_names('.pgm', PATH):
        print(mapName)
        crop_map(mapName, PATH)

if __name__ == '__main__':
    main()

