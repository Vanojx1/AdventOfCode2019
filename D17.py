from intcode import IntcodeProgram
import tkinter as tk
import re

with open('input/d17.txt') as f:
    d17_input = [int(l) for l in f.read().split(',')]

CROSSING = 0
WALKED = 1
SCAFFOLD = 35
TOP = 94
RIGHT = 62
BOTTOM = 118
LEFT = 60
SPACE = 46


class Tile(object):
    color_map = {
        CROSSING: 'blue',
        WALKED: 'gold',
        SCAFFOLD: 'green',
        TOP: 'red',   # ^
        RIGHT: 'red',   # >
        BOTTOM: 'red',  # v
        LEFT: 'red'    # <
    }

    def __init__(self, app, coords, ttype):
        self.app = app
        self.x, self.y = coords
        self.ttype = ttype
        el = self.app.canvas.create_polygon(
            *self.d_coords,
            fill=self.color_map[self.ttype],
            outline='black'
        )
        self.id = el

    @property
    def d_coords(self):
        size = self.app.tile_size
        rx = self.x*size
        ry = self.y*size
        if self.ttype in (SCAFFOLD, CROSSING, WALKED):
            return (rx, ry, rx+size, ry, rx+size, ry+size, rx, ry+size)
        elif self.ttype == TOP:
            return (rx+size/2, ry, rx+size, ry+size, rx, ry+size)
        elif self.ttype == LEFT:
            return (rx, ry+size/2, rx+size, ry, rx+size, ry+size)
        elif self.ttype == BOTTOM:
            return (rx, ry, rx+size, ry, rx+size/2, ry+size)
        elif self.ttype == RIGHT:
            return (rx, ry, rx+size, ry+size/2, rx, ry+size)

    def move(self, x, y):
        self.x, self.y = (x, y)
        self.app.canvas.coords(self.id, *self.d_coords)

    def update(self, newtype):
        self.ttype = newtype
        self.app.canvas.itemconfigure(self.id, fill=self.color_map[self.ttype])
        self.app.canvas.coords(self.id, *self.d_coords)

    def remove(self):
        self.app.canvas.delete(self.id)

    @property
    def position(self):
        return (self.x, self.y)


class App(object):
    def __init__(self, master, memory, **kwargs):
        self.master = master
        self.tile_size = 10

        self.memory = memory
        self.program = IntcodeProgram(self.memory)
        self.program.run()
        self.grid = [[]]
        for ascii_code in self.program.output[:-2]:
            if ascii_code == '10':
                self.grid.append([])
            else:
                self.grid[-1].append(int(ascii_code))

        self.width = len(self.grid[0]) * self.tile_size
        self.height = len(self.grid) * self.tile_size

        self.canvas = tk.Canvas(
            self.master,
            width=self.width,
            height=self.height,
            bg='#333'
        )
        self.canvas.pack()

        self.scaffold_mapping = {}
        self.robot = None
        for y, row in enumerate(self.grid):
            for x, col in enumerate(row):
                if col in (TOP, RIGHT, BOTTOM, LEFT):
                    self.robot = Tile(self, (x, y), col)
                elif col != SPACE:
                    self.scaffold_mapping[(x, y)] = Tile(self, (x, y), col)

        for x, y in self.scaffold_mapping.keys():
            if all([pos in self.scaffold_mapping for pos in [(x, y-1), (x+1, y), (x, y+1), (x-1, y)]]):
                self.scaffold_mapping[(x, y)].update(0)

        self.d17p1 = sum([x*y for x, y in [k for k, v in self.scaffold_mapping.items() if v.ttype == CROSSING]])

        self.moves = [LEFT, TOP, RIGHT, BOTTOM]
        self.move_offset = {
            TOP: lambda p: (p[0], p[1]-1),
            BOTTOM: lambda p: (p[0], p[1]+1),
            LEFT: lambda p: (p[0]-1, p[1]),
            RIGHT: lambda p: (p[0]+1, p[1])
        }

        self.transitions = {
            (TOP, RIGHT): 'R',
            (TOP, LEFT): 'L',
            (RIGHT, TOP): 'L',
            (RIGHT, BOTTOM): 'R',
            (BOTTOM, RIGHT): 'L',
            (BOTTOM, LEFT): 'R',
            (LEFT, TOP): 'R',
            (LEFT, BOTTOM): 'L'
        }

        self.opposite = {
            TOP: BOTTOM,
            BOTTOM: TOP,
            LEFT: RIGHT,
            RIGHT: LEFT,
        }

        self.path = []
        self.forwards = 0
        robot_start = self.robot.position
        robot_start_dir = self.robot.ttype
        self.draw_ticks = []
        while True:
            next_dir, (x, y) = self.get_next_dir()
            if next_dir is None:
                self.path.append(str(self.forwards+1))
                break
            if self.robot.ttype != next_dir:
                if self.forwards != 0:
                    self.path.append(str(self.forwards+1))
                self.forwards = 0
                self.path.append(self.transitions[(self.robot.ttype, next_dir)])
            else:
                self.forwards += 1
            self.robot.update(next_dir)
            self.robot.move(x, y)
            if self.scaffold_mapping[(x, y)].ttype != CROSSING:
                self.scaffold_mapping[(x, y)].update(WALKED)
            self.draw_ticks.append(((x, y), next_dir))

        path = ''.join(self.path)
        self.routine = self.create_routine(path) + [ord('N'), 10]
        self.memory[0] = 2

        self.program = IntcodeProgram(self.memory)
        for fn in self.routine:
            self.program.set_input(fn)
        self.program.run()

        self.d17p2 = int(self.program.output[-1])

        [s.update(SCAFFOLD) for s in self.scaffold_mapping.values()]
        self.robot.update(robot_start_dir)
        self.robot.move(*robot_start)

        self.master.after(0, self.refresh)

    def get_next_dir(self):
        pos_map = {m: self.move_offset[m](self.robot.position) for m in self.moves}
        if self.robot.position in self.scaffold_mapping and self.scaffold_mapping[self.robot.position].ttype == CROSSING:
            return self.robot.ttype, pos_map[self.robot.ttype]
        for m, pos in pos_map.items():
            if pos in self.scaffold_mapping and m != self.opposite[self.robot.ttype]:
                return m, pos
        return None, (None, None)

    def asciize(self, string):
        return list(map(int, ',44,'.join(map(lambda el: ','.join(map(lambda x: str(ord(x)), el)), re.findall(r'[A-Z]|\d+', string))).split(','))) + [10]

    def create_routine(self, path):
        strp = path
        routine = []
        char_marker = ord('A')
        while True:
            p = [m for m in re.findall(r'\w\d+', strp)]
            if len(p) == 0:
                break
            curr_test = []
            while True:
                curr_test.append(p.pop(0))
                match = [a.start() for a in re.finditer(''.join(curr_test), strp)]
                if len(match) < 3:
                    curr_test.pop()
                    break
            match = ''.join(curr_test)
            strp = re.sub(match, chr(char_marker), strp)
            # print(match, self.asciize(match), len(self.asciize(match)))
            routine += self.asciize(match)
            char_marker += 1
        # print(strp, self.asciize(strp), len(self.asciize(strp)))
        return self.asciize(strp) + routine

    def refresh(self):
        (x, y), next_dir = self.draw_ticks.pop(0)
        self.robot.update(next_dir)
        self.robot.move(x, y)
        self.scaffold_mapping[(x, y)].update(WALKED)
        if len(self.draw_ticks) > 0:
            self.master.after(20, self.refresh)


root = tk.Tk()
app = App(root, d17_input)


def d17p1():
    return app.d17p1


def d17p2():
    return app.d17p2


if __name__ == "__main__":
    print('D17P1 result:', d17p1())
    print('D17P2 result:', d17p2())
    root.mainloop()
