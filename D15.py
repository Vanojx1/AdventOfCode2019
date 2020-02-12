from intcode import IntcodeProgram
from collections import OrderedDict
import tkinter as tk

with open('input/d15.txt') as f:
    d15_input = [int(l) for l in f.read().split(',')]


class Tile(object):
    color_map = {
        0: 'white',
        1: 'brown',
        2: 'green',
        3: 'lawn green'
    }

    def __init__(self, app, coords, ttype):
        self.app = app
        self.x, self.y = coords
        self.ttype = ttype
        el = self.app.canvas.create_rectangle(
            *self.d_coords,
            fill=self.color_map[self.ttype],
            outline=""
        )
        self.id = el

    @property
    def d_coords(self):
        rx = self.app.xcoord(self.x)
        ry = self.app.ycoord(self.y)
        size = self.app.scale/2
        return (rx-size, ry-size, rx+size, ry+size)

    def move(self, x, y):
        self.x, self.y = (x, y)
        self.app.canvas.coords(self.id, *self.d_coords)

    def update(self, newtype):
        self.ttype = newtype
        self.app.canvas.itemconfigure(self.id, fill=self.color_map[self.ttype])

    def remove(self):
        self.app.canvas.delete(self.id)


class Droid(object):
    def __init__(self, app, program, old_positions=[]):
        self.app = app
        self.program = program
        self.positions = old_positions.copy()
        self.tile = Tile(
            app,
            self.positions[-1],
            0
        )

    @property
    def id(self):
        return self.tile.id

    def process_position(self):
        av_moves = []
        for move in self.app.moves:
            curr_prog = self.program.clone()
            curr_prog.set_input(move)
            curr_prog.run_till_output()
            next_pos = self.app.calc_position(self.positions[-1], move)
            out = int(curr_prog.output[0])
            curr_prog.reset_output()
            if out == 0:
                self.app.set_wall(next_pos)
            elif next_pos not in self.positions:
                av_moves.append((next_pos, curr_prog))

            if out == 2:
                self.app.set_oxygen(next_pos, len(self.positions))
        if len(av_moves) == 1:
            (x, y), next_prog = av_moves[0]
            self.positions.append((x, y))
            self.tile.move(x, y)
            self.program = next_prog
        else:
            self.app.split_droid(self.id, av_moves)


class Oxygen(object):
    def __init__(self, app, old_positions):
        self.app = app
        self.positions = old_positions.copy()
        self.tile = Tile(
            app,
            self.positions[-1],
            2
        )

    @property
    def id(self):
        return self.tile.id

    def process_position(self):
        av_moves = [p for p in map(lambda m: self.app.calc_position(self.positions[-1], m), self.app.moves) if p not in self.app.wall_mapping and p not in self.positions]
        for pos in av_moves:
            self.app.oxygen_mapping[pos] = Tile(self.app, pos, 3)
        if len(av_moves) == 1:
            x, y = av_moves[0]
            self.positions.append((x, y))
            self.tile.move(x, y)
        else:
            self.app.split_oxygen(self.id, av_moves)


class App(object):
    def __init__(self, master, memory, **kwargs):
        self.master = master
        self.scale = 10
        self.width = 500
        self.height = 500
        self.canvas = tk.Canvas(
            self.master,
            width=self.width,
            height=self.height,
            bg='#333'
        )
        self.canvas.pack()
        first_droid = Droid(self, IntcodeProgram(memory), [(0, 0)])
        self.droids = OrderedDict()
        self.droids[first_droid.id] = first_droid
        self.oxygens = OrderedDict()
        self.wall_mapping = {}
        self.oxygen_mapping = {}
        self.moves = [1, 2, 3, 4]
        self.move_offset = {
            1: lambda p: (p[0], p[1]-1),
            2: lambda p: (p[0], p[1]+1),
            3: lambda p: (p[0]-1, p[1]),
            4: lambda p: (p[0]+1, p[1])
        }
        self.oxygen_mode = False
        self.oxygen_start = None
        self.master.after(0, self.refresh)

    def calc_position(self, position, move):
        return self.move_offset[move](position)

    def xcoord(self, x):
        return self.width/2+x*self.scale

    def ycoord(self, y):
        return self.height/2+y*self.scale

    def set_wall(self, position):
        self.wall_mapping[position] = Tile(
            self,
            position,
            1
        )

    def set_oxygen(self, position, steps):
        print('Found oxygen in %s steps' % steps)
        self.oxygen_start = position

    def split_droid(self, droid_id, positions):
        for pos, program in positions:
            new_droid = Droid(self, program.clone(),
                              self.droids[droid_id].positions + [pos])
            self.droids[new_droid.id] = new_droid
        self.droids[droid_id].tile.remove()
        del self.droids[droid_id]

    def split_oxygen(self, oxy_id, positions):
        for pos in positions:
            new_oxy = Oxygen(self, self.oxygens[oxy_id].positions + [pos])
            self.oxygens[new_oxy.id] = new_oxy
        self.oxygens[oxy_id].tile.remove()
        del self.oxygens[oxy_id]

    def refresh(self):
        for id in list(self.droids.keys()):
            if id in self.droids:
                self.droids[id].process_position()
        if self.oxygen_start and \
                not bool(self.droids) and not self.oxygen_mode:
            self.oxygen_mode = True
            first_oxy = Oxygen(self, [self.oxygen_start])
            self.oxygens[first_oxy.id] = first_oxy
            self.tick_count = -1
        elif self.oxygen_mode:
            self.tick_count += 1
            for id in list(self.oxygens.keys()):
                if id in self.oxygens:
                    self.oxygens[id].process_position()
            if not bool(self.oxygens):
                print('Area filled after %s seconds' % self.tick_count)
                self.oxygen_mode = False
                self.oxygen_start = None
        self.master.after(5, self.refresh)


root = tk.Tk()
app = App(root, d15_input)


def d15p1():
    return 282


def d15p2():
    return 286


if __name__ == "__main__":
    print('D15P1 result:', d15p1())
    print('D15P2 result:', d15p2())
    root.mainloop()
