from intcode import IntcodeProgram

with open('input/d5.txt') as f:
    d5_input = [int(l) for l in f.read().split(',')]


def d5p1():
    ip = IntcodeProgram(d5_input, 1)
    ip.run()
    return int(''.join(ip.output))


def d5p2():
    ip = IntcodeProgram(d5_input, 5)
    ip.run()
    return int(''.join(ip.output))


if __name__ == '__main__':
    print('D5P1 result:', d5p1())
    print('D5P2 result:', d5p2())
