import math
from tkinter import Canvas, YES, BOTH, Tk
from collections import defaultdict

with open('input/d10.txt') as f:
    d10_input = [list(l.replace('\n', '')) for l in f.readlines()]

scale = 20
padd = 50

root = Tk()
canvas = Canvas(root, width=len(d10_input[0])*scale+padd*2,
                height=len(d10_input)*scale+padd*2, bg='white')
canvas.pack(expand=YES, fill=BOTH)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pos_mapping = defaultdict(list)
        self.destroyed = False
        self.firing = False
        self.el = canvas.create_oval(
            *self.get_point(True), fill='gray', outline=None)
        self.curr_laser = None

    def angle(self, p2):
        return round((math.degrees(math.atan2(
            p2.y-self.y,
            p2.x-self.x
        )) + 90) % 360, 2)

    def distance(self, p2):
        return round(math.sqrt(
            math.pow(self.x-p2.x, 2) +
            math.pow(self.y-p2.y, 2)
        ), 2)

    def get_point(self, arc=False):
        if arc:
            return (
                padd+self.x*scale-scale/4,
                padd+self.y*scale-scale/4,
                padd+self.x*scale+scale/4,
                padd+self.y*scale+scale/4
            )
        return (padd+self.x*scale, padd+self.y*scale)

    def select(self, color='red'):
        canvas.itemconfig(self.el, fill=color)

    def destroy(self):
        self.destroyed = True
        canvas.delete(self.el)

    def __repr__(self):
        return '(%s, %s)' % (self.x, self.y)


asteroids = {}
for y, row in enumerate(d10_input):
    for x, col in enumerate(row):
        if col == '#':
            asteroids[(x, y)] = Point(x, y)

for t in asteroids.values():
    for k, a in asteroids.items():
        if k != (t.x, t.y):
            t.pos_mapping[t.angle(a)].append(a)
            t.pos_mapping[t.angle(a)].sort(key=lambda a: a.distance(t))

maxa = max(asteroids, key=lambda a: len(asteroids[a].pos_mapping.keys()))
base = asteroids[maxa]
base.select()

base.pos_mapping = sorted(base.pos_mapping.values(),
                          key=lambda v: base.angle(v[0]))


def d10p1():
    return len(base.pos_mapping)


def d10p2():
    th200 = base.pos_mapping[199][0]
    return th200.x*100+th200.y


def animate(index=0):
    onsight = [
        p for
        p in base.pos_mapping[index % len(base.pos_mapping)]
        if not p.destroyed
    ]
    if len(onsight) > 0:
        onsight[0].destroy()
    if any([any([not p.destroyed for p in v]) for v in base.pos_mapping]):
        root.after(20, lambda: animate(index+1))


if __name__ == "__main__":
    print('D10P1 result:', d10p1())
    print('D10P2 result:', d10p2())

    root.after(0, animate)
    root.mainloop()
