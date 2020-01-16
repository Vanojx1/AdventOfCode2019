# from PIL import Image, ImageDraw
import numpy

with open('input/d3.txt') as f:
    d3_input = [l.rstrip('\n').split(',') for l in f.readlines()]


def get_distance(p1, p2):
    return abs(p2[1] - p1[1]) + abs(p2[0] - p1[0])


moves = {
    'U': lambda p, dist: (p[0], p[1]-dist),
    'R': lambda p, dist: (p[0]+dist, p[1]),
    'D': lambda p, dist: (p[0], p[1]+dist),
    'L': lambda p, dist: (p[0]-dist, p[1])
}

iters = {
    'U': lambda p, dist: iter((p[0], p[1]-i, i) for i in range(1, dist+1)),
    'R': lambda p, dist: iter((p[0]+i, p[1], i) for i in range(1, dist+1)),
    'D': lambda p, dist: iter((p[0], p[1]+i, i) for i in range(1, dist+1)),
    'L': lambda p, dist: iter((p[0]-i, p[1], i) for i in range(1, dist+1)),
}

maxx = 0
maxy = 0

for wire_index, wire in enumerate(d3_input):
    cpos = (0, 0)
    for move in wire:
        mdir, mdist = move[0], int(move[1:])
        oldp = cpos
        cpos = moves[mdir](cpos, mdist)
        maxx = max(maxx, abs(cpos[0]))
        maxy = max(maxy, abs(cpos[1]))


def d3p1():
    bitmap = numpy.full((maxy*2+1, maxx*2+1), '#')

    min_distance = float('inf')
    # img = Image.new('RGB', (maxx * 2, maxy * 2), "white")
    # colors = [(245, 66, 66), (42, 219, 71)]
    # draw = ImageDraw.Draw(img)
    # draw.line((maxx-15, maxy-15, maxx+15, maxy+15), fill=(0, 0, 0), width=15)
    # draw.line((maxx+15, maxy-15, maxx-15, maxy+15), fill=(0, 0, 0), width=15)
    for wire_index, wire in enumerate(d3_input):
        cpos = (0, 0)
        for move in wire:
            mdir, mdist = move[0], int(move[1:])
            ox, oy = cpos
            for x, y, i in iters[mdir](cpos, mdist):
                rx = x+maxx
                ry = y+maxy
                if bitmap[ry][rx] != '#' and bitmap[ry][rx] != str(wire_index):
                    min_distance = min(
                        min_distance, get_distance((0, 0), (x, y)))
                    # draw.line((x+maxx-15, y+maxy-15, x+maxx+15,
                    #            y+maxy+15), fill=(0, 0, 0), width=15)
                    # draw.line((x+maxx+15, y+maxy-15, x+maxx-15,
                    #            y+maxy+15), fill=(0, 0, 0), width=15)
                    bitmap[ry][rx] = 'X'
                else:
                    bitmap[ry][rx] = str(wire_index)
            cpos = moves[mdir](cpos, mdist)
            ox, x = map(lambda i: i+maxx, [ox, x])
            oy, y = map(lambda i: i+maxy, [oy, y])
            # draw.line((ox, oy, x, y), fill=colors[wire_index], width=5)
    # img.show()
    return min_distance


def d3p2():
    bitmap = numpy.full((maxy*2+1, maxx*2+1), '#')

    intercept_mapping = {}
    # img = Image.new('RGB', (maxx * 2, maxy * 2), "white")
    # colors = [(245, 66, 66), (42, 219, 71)]
    # draw = ImageDraw.Draw(img)
    # draw.line((maxx-15, maxy-15, maxx+15, maxy+15), fill=(0, 0, 0), width=15)
    # draw.line((maxx+15, maxy-15, maxx-15, maxy+15), fill=(0, 0, 0), width=15)
    for wire_index, wire in enumerate(d3_input):
        cpos = (0, 0)
        wire_length = 0
        for move in wire:
            mdir, mdist = move[0], int(move[1:])
            ox, oy = cpos
            for x, y, cdist in iters[mdir](cpos, mdist):
                rx = x+maxx
                ry = y+maxy
                if bitmap[ry][rx] != '#' and bitmap[ry][rx] != str(wire_index):
                    intercept_mapping[(x, y)] = {}
                    # draw.line((x+maxx-15, y+maxy-15, x+maxx+15,
                    #            y+maxy+15), fill=(0, 0, 0), width=15)
                    # draw.line((x+maxx+15, y+maxy-15, x+maxx-15,
                    #            y+maxy+15), fill=(0, 0, 0), width=15)
                    bitmap[ry][rx] = 'X'
                else:
                    bitmap[ry][rx] = str(wire_index)
            wire_length += abs(mdist)
            cpos = moves[mdir](cpos, mdist)
            ox, x = map(lambda i: i+maxx, [ox, x])
            oy, y = map(lambda i: i+maxy, [oy, y])
            # draw.line((ox, oy, x, y), fill=colors[wire_index], width=5)

    for wire_index, wire in enumerate(d3_input):
        cpos = (0, 0)
        wire_length = 0
        for move in wire:
            mdir, mdist = move[0], int(move[1:])
            for x, y, cdist in iters[mdir](cpos, mdist):
                if tuple([x, y]) in intercept_mapping.keys():
                    intercept_mapping[(x, y)][wire_index] = wire_length + cdist
            wire_length += abs(mdist)
            cpos = moves[mdir](cpos, mdist)

    # img.show()
    return min(map(lambda i: i[0]+i[1], intercept_mapping.values()))


if __name__ == '__main__':
    print('D3P1 result:', d3p1())
    print('D3P2 result:', d3p2())
