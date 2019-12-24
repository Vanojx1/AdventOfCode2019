with open('input/d1.txt') as f:
    d1_input = [l.rstrip('\n') for l in f.readlines()]

result = sum(map(lambda mass: int(int(mass)/3)-2, d1_input))

print('D1P1 result:', result)


def fuel_calc(mass):
    f = max(0, int(int(mass)/3)-2)
    if f == 0:
        return f
    return f + fuel_calc(f)


result = sum(map(fuel_calc, d1_input))

print('D1P2 result:', result)
