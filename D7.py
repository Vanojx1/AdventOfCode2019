from itertools import permutations
from intcode import IntcodeProgram

with open('input/d7.txt') as f:
    d7_input = [int(l) for l in f.read().split(',')]


highest_signal = 0
for settings in permutations(range(5), 5):
    curr_signal = 0
    for curr_setting in settings:
        ip = IntcodeProgram(d7_input, curr_setting)
        ip.set_input(curr_signal)
        ip.run()
        curr_signal = int(ip.get_output())
    highest_signal = max(highest_signal, curr_signal)

print('D7P1 result:', highest_signal)


highest_signal = 0
for settings in permutations(range(5, 10)):
    curr_signal = 0
    ip_mapping = list(map(lambda curr_setting: IntcodeProgram(
        d7_input, curr_setting), settings))
    while all(not ip.halted for ip in ip_mapping):
        for ip in ip_mapping:
            ip.set_input(curr_signal)
            ip.run(True)
            out = ip.get_output()
            if not ip.halted and out != '':
                curr_signal = int(out)
    highest_signal = max(highest_signal, curr_signal)

print('D7P2 result:', highest_signal)
