from collections import defaultdict
from PIL import Image, ImageDraw

with open('input/d8.txt') as f:
    d8_input = [int(l) for l in list(f.read())]

width = 25
height = 6


def get_layers(image, w, h):
    while 1:
        curr_layer = []
        for _ in range(h):
            curr_layer.append(image[:w])
            del image[:w]
        yield curr_layer
        if len(image) == 0:
            break


def get_pixels(layer):
    mapping = defaultdict(int)
    for row in layer:
        for col in row:
            mapping[col] += 1
    return mapping


layers = list(get_layers(d8_input, width, height))


def d8p1():
    layers_pixels = [get_pixels(l) for l in layers]
    fewest_0_layer = min(layers_pixels, key=lambda l: l[0])
    return fewest_0_layer[1] * fewest_0_layer[2]


def d8p2():
    color_map = {0: (255, 255, 255, 0), 1: (0, 0, 0, 255), 2: (0, 0, 0, 0)}

    def merge_pixel(layers, x, y):
        pixel = None
        for layer in layers[::-1]:
            if pixel is None or layer[y][x] != 2:
                pixel = layer[y][x]
        return pixel

    merged_layers = [[merge_pixel(layers, x, y)
                      for x in range(width)] for y in range(height)]

    padding = 5

    img = Image.new('RGBA', (width+padding*2, height+padding*2))
    draw = ImageDraw.Draw(img)
    for y in range(height):
        for x in range(width):
            draw.point((x+padding, y+padding),
                       fill=color_map[merged_layers[y][x]])

    img = img.resize((width*50, height*50), Image.ANTIALIAS)

    # img.show()

    return 'KCGEC'


if __name__ == "__main__":
    print('D8P1 result:', d8p1())
    print('D8P1 result:', d8p2())
