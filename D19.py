from intcode import IntcodeProgram
import tkinter as tk

with open('input/d19.txt') as f:
    d19_input = [int(l) for l in f.read().split(',')]

BEAM = '1'
SPACE = '0'
VERTEX = 'V'


class Tile(object):
    color_map = {
        BEAM: 'white',
        SPACE: '#333',
        VERTEX: 'red',
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
        return (rx, ry, rx+size, ry, rx+size, ry+size, rx, ry+size)


class App(object):
    def __init__(self, master, memory, **kwargs):
        self.master = master
        self.memory = memory

        self.square_size = 100
        self.tile_size = 6
        self.minx = 0
        self.diff = self.square_size-1

        self.p1 = None
        self.p2 = None

        bottom_left = None
        total_beam_points = 0
        y = 0
        while True:
            x = self.first_beam(y)
            if x == -1:
                y += 1
                continue
            if y < 50:
                total_beam_points += self.last_beam(x, y) - x
            if self.get_point(x+self.diff, y-self.diff) == 1:
                bottom_left = (x, y)
                break
            y += 1

        self.closest_point = (bottom_left[0], bottom_left[1]-self.diff)

        self.p1 = total_beam_points
        self.p2 = self.closest_point[0]*10000 + self.closest_point[1]

        self.master.after(0, self.refresh)

    def refresh(self):
        self.area = []
        self.tiles = {}
        for y in range(self.square_size+40):
            self.area.append([])
            for x in range(self.square_size+40):
                rx, ry = self.offset_point(x, y)
                r = self.get_point(rx, ry)
                self.area[y].append(r)
                self.tiles[(x, y)] = str(r)

        self.width = len(self.area[0]) * self.tile_size
        self.height = len(self.area) * self.tile_size

        self.canvas = tk.Canvas(
            self.master,
            width=self.width,
            height=self.height,
            bg='#333'
        )
        self.canvas.pack()

        for pos, ttype in self.tiles.items():
            rx, ry = self.offset_point(*pos)
            if (self.closest_point[0] <= rx <= self.closest_point[0]+self.square_size-1) and (self.closest_point[1] <= ry <= self.closest_point[1]+self.square_size-1):
                Tile(self, pos, VERTEX)
            else:
                Tile(self, pos, ttype)

        self.canvas.pack()

    def offset_point(self, x, y):
        return (
            x+self.closest_point[0]-20,
            y+self.closest_point[1]-20
        )

    def first_beam(self, y):
        x = self.minx
        while True:
            r = self.get_point(x, y)
            if x > self.minx+100:
                return -1
            if r == 1:
                self.minx = x
                return x
            x += 1

    def last_beam(self, first_x, y):
        x = first_x+1
        while True:
            r = self.get_point(x, y)
            if r == 0:
                return x
            x += 1

    def get_point(self, x, y):
        ip = IntcodeProgram(self.memory)
        ip.set_input(x)
        ip.set_input(y)
        ip.run()
        return int(ip.output[0])


root = tk.Tk()
app = App(root, d19_input)


def d19p1():
    return app.p1


def d19p2():
    return app.p2


if __name__ == "__main__":
    print('D19P1 result:', d19p1())
    print('D19P2 result:', d19p2())
    root.mainloop()
