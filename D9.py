from intcode import IntcodeProgram

with open('input/d9.txt') as f:
    d9_input = [int(l) for l in f.read().split(',')]


def d9p1():
    ip = IntcodeProgram(d9_input, 1)
    ip.run()
    return int(''.join(ip.output))


def d9p2():
    ip = IntcodeProgram(d9_input, 2)
    ip.run()
    return int(''.join(ip.output))


if __name__ == "__main__":
    print('D9P1 result:', d9p1())
    print('D9P2 result:', d9p2())
