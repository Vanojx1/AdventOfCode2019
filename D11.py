from intcode import IntcodeProgram
from collections import defaultdict
from PIL import Image, ImageDraw

with open('input/d11.txt') as f:
    d9_input = [int(l) for l in f.read().split(',')]

dirs = ['^', '>', 'v', '<']
dirs_move = {
    '^': lambda p: (p[0], p[1]-1),
    '>': lambda p: (p[0]+1, p[1]),
    'v': lambda p: (p[0], p[1]+1),
    '<': lambda p: (p[0]-1, p[1])
}


def cycle(ip, current_color):
    ip.set_input(current_color)
    ip.run_till_output()
    o1 = int(''.join(ip.output) or 0)
    ip.reset_output()
    ip.run_till_output()
    o2 = int(''.join(ip.output) or 0)
    ip.reset_output()
    return o1, o2, ip.halted


def paint(starting_panel_color):
    ip = IntcodeProgram(d9_input)
    dir_index = 0
    robot_pos = (0, 0)
    panels = defaultdict(int)
    panels[robot_pos] = starting_panel_color
    while 1:
        color, next_dir, halted = cycle(ip, panels[robot_pos])
        if halted:
            break
        panels[robot_pos] = color
        dir_index += 1 if next_dir else -1
        robot_pos = dirs_move[dirs[dir_index % 4]](robot_pos)
    return panels


def d11p1():
    panels = paint(0)
    return len(panels.keys())


def d11p2():
    panels = paint(1)
    maxw, maxh = (0, 0)
    for x, y in panels.keys():
        maxw = max(maxw, x*2)
        maxh = max(maxh, y*2)

    padding = 5
    width = maxw+padding*2
    height = maxh+padding*2
    img = Image.new('RGBA', (width, height), color="white")
    draw = ImageDraw.Draw(img)

    for (x, y), color in panels.items():
        draw.point((x+padding, y+padding), fill='black' if color else None)

    img = img.resize((width*50, height*50), Image.ANTIALIAS)

    # img.show()

    return 'HKJBAHCR'


if __name__ == "__main__":
    print('D11P1 result:', d11p1())
    print('D11P2 result:', d11p2())
