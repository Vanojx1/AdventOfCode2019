from intcode import IntcodeProgram

with open('input/d9.txt') as f:
    d9_input = [int(l) for l in f.read().split(',')]

ip = IntcodeProgram(d9_input, 1)
ip.run()

print('D9P1 result:', ip.get_output())

ip = IntcodeProgram(d9_input, 2)
ip.run()

print('D9P2 result:', ip.get_output())
