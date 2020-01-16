import re
import sys
import math
from itertools import permutations

from OpenGL.GL import (
    glClear,
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    glPushMatrix,
    glMaterialfv,
    GL_DIFFUSE,
    glTranslatef,
    glPopMatrix,
    GL_FRONT,
    glClearColor,
    glShadeModel,
    GL_SMOOTH,
    GL_CULL_FACE,
    glEnable,
    GL_DEPTH_TEST,
    GL_LIGHTING,
    glLightfv,
    GL_LIGHT0,
    GL_POSITION,
    glLightf,
    GL_CONSTANT_ATTENUATION,
    GL_LINEAR_ATTENUATION,
    glMatrixMode,
    GL_PROJECTION,
    GL_MODELVIEW,
)
from OpenGL.GLU import gluPerspective, gluLookAt
from OpenGL.GLUT import (
    glutSolidSphere,
    glutPostRedisplay,
    glutDisplayFunc,
    glutSwapBuffers,
    glutTimerFunc,
    glutInit,
    glutInitDisplayMode,
    GLUT_DOUBLE,
    GLUT_RGB,
    GLUT_DEPTH,
    glutInitWindowSize,
    glutInitWindowPosition,
    glutCreateWindow,
    glutMainLoop
)

with open('input/d12.txt') as f:
    d12_input = [tuple(int(p) for p in re.search(
        r'<\w=(-?\d+), \w=(-?\d+), \w=(-?\d+)>',
        l.replace('\n', '')).groups()) for l in f.readlines()]


class Moon:

    def __init__(self, pos):
        self.x, self.y, self.z = pos
        self.vx, self.vy, self.vz = (0, 0, 0)
        self.sphere = None

    @property
    def kinetic_energy(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    @property
    def potential_energy(self):
        return abs(self.vx) + abs(self.vy) + abs(self.vz)

    @property
    def stringify(self):
        return '|'.join([
            str(self.x),
            str(self.y),
            str(self.z),
            str(self.vx),
            str(self.vy),
            str(self.vz)
        ])

    def __repr__(self):
        return 'pos=<x= %s, y= %s, z=%s>, vel=<x=%s, y=%s, z= %s>' % (
            self.x,
            self.y,
            self.z,
            self.vx,
            self.vy,
            self.vz
        )


def apply_gravity(curr_moons):
    for m1, m2 in permutations(curr_moons, 2):
        if m1.x != m2.x:
            m1.vx += 1 if m1.x < m2.x else -1
        if m1.y != m2.y:
            m1.vy += 1 if m1.y < m2.y else -1
        if m1.z != m2.z:
            m1.vz += 1 if m1.z < m2.z else -1


def apply_velocity(curr_moons):
    for m in curr_moons:
        m.x += m.vx
        m.y += m.vy
        m.z += m.vz


def d12p1():
    moons = [Moon(pos) for pos in d12_input]
    for _ in range(1000):
        apply_gravity(moons)
        apply_velocity(moons)
    return sum(map(lambda m: m.kinetic_energy * m.potential_energy, moons))


def lcm(a, b):
    return (a*b)//math.gcd(a, b)


def d12p2():
    moons = [Moon(pos) for pos in d12_input]
    xpos, ypos, zpos = [set(), set(), set()]
    repeated = {'x': 0, 'y': 0, 'z': 0}
    count = 0
    while 1:
        apply_gravity(moons)
        apply_velocity(moons)
        xs = '|'.join([str([m.x, m.vx]) for m in moons])
        ys = '|'.join([str([m.y, m.vy]) for m in moons])
        zs = '|'.join([str([m.z, m.vz]) for m in moons])

        if xs not in xpos:
            xpos.add(xs)
        elif repeated['x'] == 0:
            repeated['x'] = count

        if ys not in ypos:
            ypos.add(ys)
        elif repeated['y'] == 0:
            repeated['y'] = count

        if zs not in zpos:
            zpos.add(zs)
        elif repeated['z'] == 0:
            repeated['z'] = count

        if all([v > 0 for v in repeated.values()]):
            break
        count += 1

    return lcm(lcm(repeated['x'], repeated['y']), repeated['z'])


colors = [[1.0, 0.0, 0.0, 1.0], [0.0, 1.0, 0.0, 1.0],
          [0.0, 0.0, 1.0, 1.0], [0.0, 0.2, 0.0, 1.0]]


def display_scene(curr_moons):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    glTranslatef(0, 0, 0)
    glutSolidSphere(.2, 60, 20)
    glPopMatrix()
    for index, m in enumerate(curr_moons):
        glPushMatrix()
        glMaterialfv(GL_FRONT, GL_DIFFUSE, colors[index])
        glTranslatef(m.x/10, m.y/10, m.z/10)
        glutSolidSphere(.1, 60, 20)
        glPopMatrix()
    apply_gravity(curr_moons)
    apply_velocity(curr_moons)
    glutSwapBuffers()


def timer(extra):
    glutPostRedisplay()
    glutTimerFunc(120, timer, 0)


def main():
    moons = [Moon(pos) for pos in d12_input]
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 800)
    glutInitWindowPosition(350, 200)
    glutCreateWindow('name')
    glClearColor(0., 0., 0., 1.)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    lightZeroPosition = [10., 4., 10., 1.]
    lightZeroColor = [0.8, 1.0, 0.8, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
    glEnable(GL_LIGHT0)
    glutDisplayFunc(lambda: display_scene(moons))
    glutTimerFunc(0, timer, 0)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(40., 1., 1., 40.)
    glMatrixMode(GL_MODELVIEW)
    gluLookAt(0, -10, 10,
              0, 0, 0,
              0, 1, 0)
    glPushMatrix()
    glutMainLoop()


if __name__ == "__main__":
    print('D12P1 result:', d12p1())
    print('D12P2 result:', d12p2())
    main()
