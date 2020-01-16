from itertools import product
from intcode import IntcodeProgram

with open('input/d2.txt') as f:
    d2_input = [int(l) for l in f.read().split(',')]


def d2p1():
    ip = IntcodeProgram(d2_input)
    ip.run()
    return ip.intcode[0]


def d2p2():
    prod = product(range(100), range(100))
    result = None
    for noun, verb in prod:
        ip = IntcodeProgram(d2_input)
        ip.intcode[1], ip.intcode[2] = noun, verb
        while not ip.halted:
            ip.next()
            if ip.intcode[0] == 19690720:
                result = int(str(noun).zfill(2) + str(verb).zfill(2))
                break
    return result


if __name__ == '__main__':
    print('D2P1 result:', d2p1())
    print('D2P2 result:', d2p2())
