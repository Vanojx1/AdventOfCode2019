from itertools import accumulate

with open('input/d16.txt') as f:
    d16_input = [int(l) for l in list(f.read())]

pattern = [0, 1, 0, -1]


def d16p1():
    next_phase = d16_input.copy()
    for _ in range(100):
        next_phase = [int(str(sum([a*b for a, b in zip(next_phase, [pattern[int(i/k) % 4] for i in range(len(next_phase)+1)][1:])]))[-1]) for k in range(1, len(next_phase)+1)]
    return int(''.join(map(str, next_phase[:8])))


def d16p2():
    next_phase = d16_input.copy()
    offset = int(''.join(map(str, next_phase[:7])))
    next_phase = (next_phase*10000)[offset:][::-1]

    for _ in range(100):
        next_phase = list(accumulate(next_phase, lambda a, b: (a+b) % 10))

    return int(''.join(map(str, next_phase[::-1][:8])))


if __name__ == "__main__":
    print('D16P1 result:', d16p1())
    print('D16P2 result:', d16p2())
