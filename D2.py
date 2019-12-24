from itertools import product
from intcode import IntcodeProgram

with open('input/d2.txt') as f:
    d2_input = [int(l) for l in f.read().split(',')]

ip = IntcodeProgram(d2_input)
ip.run()

print('D2P1 result:', ip.intcode[0])

prod = product(range(100), range(100))
result = None
for noun, verb in prod:
    ip = IntcodeProgram(d2_input)
    ip.intcode[1], ip.intcode[2] = noun, verb
    while not ip.halted:
        ip.next()
        if ip.intcode[0] == 19690720:
            result = str(noun).zfill(2) + str(verb).zfill(2)
            break

print('D2P2 result:', result)
