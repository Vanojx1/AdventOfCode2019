with open('input/d1.txt') as f:
    d1_input = [l.rstrip('\n') for l in f.readlines()]


def d1p1():
    return sum(map(lambda mass: int(int(mass)/3)-2, d1_input))


def fuel_calc(mass):
    f = max(0, int(int(mass)/3)-2)
    if f == 0:
        return f
    return f + fuel_calc(f)


def d1p2():
    return sum(map(fuel_calc, d1_input))


if __name__ == '__main__':
    print('D1P1 result:', d1p2())
    print('D1P2 result:', d1p2())
