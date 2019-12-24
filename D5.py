from intcode import IntcodeProgram

with open('input/d5.txt') as f:
    d5_input = [int(l) for l in f.read().split(',')]

ip = IntcodeProgram(d5_input, 1)
ip.run()

print('D5P1 result:', ip.output)

ip = IntcodeProgram(d5_input, 5)
ip.run()

print('D5P2 result:', ip.output)
