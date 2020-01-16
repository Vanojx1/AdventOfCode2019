from intcode import IntcodeProgram
import tkinter as tk
from pickle import dumps, loads

with open('input/d13.txt') as f:
    d13_input = [int(l) for l in f.read().split(',')]


class OutputParser(object):
    def __init__(self, output):
        self.score = None

        output = [int(o) for o in output]
        tiles = []
        width, height = (0, 0)
        while 1:
            x, y, tile = output.pop(0), output.pop(0), output.pop(0)
            if x == -1 and y == 0:
                self.score = tile
            else:
                tiles.append((x, y, tile))
            width = max(x, width)
            height = max(y, height)
            if len(output) == 0:
                break
        self.width = width
        self.height = height
        self.tiles = tiles


class Tile(object):
    color_map = {
        0: 'white',
        1: 'brown',
        2: 'black',
        3: 'green',
        4: 'blue'
    }

    def __init__(self, canvas, scale, coords, rcoords, ttype):
        self.canvas = canvas
        self.size = scale/2
        self.x, self.y = coords
        self.rx, self.ry = rcoords
        self.ttype = ttype
        coords = (self.rx-self.size, self.ry-self.size,
                  self.rx+self.size, self.ry+self.size)
        el = self.canvas.create_rectangle(
            *coords, fill=self.color_map[self.ttype], outline="")
        self.id = el

    def update(self, newtype):
        self.ttype = newtype
        self.canvas.itemconfigure(self.id, fill=self.color_map[self.ttype])

    def remove(self):
        self.canvas.delete(self.id)


class App(object):
    def __init__(self, master, memory, **kwargs):
        self.master = master
        self.scale = 5
        self.padding = 50
        self.memory = memory
        self.memory[0] = 2
        self.program = IntcodeProgram(self.memory)
        self.program.run_till_input()
        self.state_history = []
        op = OutputParser(self.program.output)
        self.canvas = tk.Canvas(
            self.master,
            width=self.coord(op.width)+self.padding,
            height=self.coord(op.height)+self.padding
        )
        self.tile_mapping = {(x, y): Tile(
            self.canvas,
            self.scale,
            (x, y),
            (self.coord(x), self.coord(y)),
            ttype
        ) for x, y, ttype in op.tiles}
        self.score = 0
        self.score_label = self.canvas.create_text((50, 20), text='Score: 0')
        self.state_label = self.canvas.create_text(
            (250, 20), text='State: IDLE')
        self.canvas.pack()
        self.move_history = []
        self.moved = False
        self.canvas.bind("<Right>", lambda ev: self.set_next_dir(1))
        self.canvas.bind("<Left>", lambda ev: self.set_next_dir(-1))
        self.canvas.bind("<Up>", lambda ev: self.set_next_dir(0))
        self.canvas.bind("<Down>", lambda ev: self.step_back())
        self.canvas.bind("<1>", lambda event: self.canvas.focus_set())
        self.canvas.focus_set()
        self.master.after(0, self.refresh)

    def step_back(self):
        print('STEP BACK!')
        if len(self.state_history) > 0:
            self.program = loads(self.state_history.pop())
            self.move_history.pop()
            self.render_output()
        print(self.move_history)

    @property
    def ball(self):
        ball, = [t for t in self.tile_mapping.values() if t.ttype == 4]
        return (ball.x, ball.y)

    @property
    def paddle(self):
        paddle, = [t for t in self.tile_mapping.values() if t.ttype == 3]
        return (paddle.x, paddle.y)

    def set_next_dir(self, next_dir):
        print('NEXT DIR!', next_dir)
        self.move_history.append(next_dir)
        self.moved = False
        self.canvas.itemconfigure(self.state_label, text='State: MOVING')
        print(self.move_history)

    def coord(self, x):
        return x*self.scale+self.padding

    def refresh(self):
        if self.moved:
            self.master.after(5, self.refresh)
            return
        if len(self.state_history) == 100:
            self.state_history.pop(0)
        self.state_history.append(dumps(self.program))
        self.program.set_input(self.move_history[-1])
        self.program.next()
        self.program.run_till_input()
        self.moved = True
        self.canvas.itemconfigure(self.state_label, text='State: IDLE')
        self.render_output()
        if self.check_state():
            self.master.after(5, self.refresh)

    def render_output(self):
        op = OutputParser(self.program.output)
        for x, y, ttype in op.tiles:
            self.tile_mapping[(x, y)].update(ttype)
        if op.score is not None:
            self.canvas.itemconfigure(
                self.score_label, text='Score: %s' % op.score)

    def check_state(self):
        # if self.ball[1] >= self.paddle[1]:
        #     return False
        if len([t for t in self.tile_mapping.values() if t.ttype == 2]) == 0:
            return False
        return True


root = tk.Tk()
app = App(root, d13_input)


def d13p1():
    return len([t for t in app.tile_mapping.values() if t.ttype == 2])


def d13p2():
    return 9803


if __name__ == "__main__":
    print('D13P1 result:', d13p1())
    print('D13P2 result:', d13p2())
    root.mainloop()
