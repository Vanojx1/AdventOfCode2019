import re
import math
from collections import defaultdict

with open('input/d14.txt') as f:
    d14_input = [l.rstrip('\n') for l in f.readlines()]


class Chemical:

    def __init__(self, factory, reaction_string):
        rlist = [(int(i), c) for i, c in re.findall(
            r'(?:, )?(?:(\d+) ([A-Z]+))(?:, )?', reaction_string)]
        self.factory = factory
        self.quant_per_craft, self.chem = rlist.pop()
        self.chem_required = rlist

    def craft(self, quant):
        if self.chem == 'ORE':
            return quant
        if self.factory.chem_storage[self.chem] > 0:
            rquant = quant - min(quant, self.factory.chem_storage[self.chem])
            self.factory.chem_storage[self.chem] -= quant - rquant
        else:
            rquant = quant
        craftings = math.ceil(rquant / self.quant_per_craft)
        self.factory.chem_storage[self.chem] += self.quant_per_craft * \
            craftings - rquant
        to_craft = [(q * craftings, c) for q, c in self.chem_required]
        return sum(map(
            lambda r: self.factory.chemicals[r[1]].craft(r[0]),
            to_craft))

    def __repr__(self):
        return '%s=%s' % (
            '+'.join(['%s%s' % (i, c) for i, c in self.chem_required]),
            '%s%s' % (self.quant_per_craft, self.chem))


class Nanofactory:
    def __init__(self, rlist):
        self.chemicals = {r.chem: r for r in [
            Chemical(self, r) for r in rlist.copy()]}
        self.chemicals['ORE'] = Chemical(self, '1 ORE')
        self.chem_storage = defaultdict(int)

    def craft(self, quant, chem):
        return self.chemicals[chem].craft(quant)


factory = Nanofactory(d14_input)
ore_per_craft = factory.craft(1, 'FUEL')


def d14p1():
    factory = Nanofactory(d14_input)
    return factory.craft(1, 'FUEL')


def d14p2():
    # ALGORITHMICLESS SOLUTION LEWL
    available_ore = 1000000000000  # 13
    uom = 1
    k = 9
    while True:
        factory = Nanofactory(d14_input)
        ore = factory.craft(k ** uom, 'FUEL')
        if ore > available_ore:
            break
        uom += 1
    n = k**uom
    closer = None
    while True:
        factory = Nanofactory(d14_input)
        ore = factory.craft(n, 'FUEL')
        if ore < available_ore:
            closer = n
            break
        n -= 10000
    while True:
        factory = Nanofactory(d14_input)
        ore = factory.craft(closer, 'FUEL')
        if ore > available_ore:
            break
        closer += 1000
    closer -= 1000
    while True:
        factory = Nanofactory(d14_input)
        ore = factory.craft(closer, 'FUEL')
        if ore > available_ore:
            break
        closer += 1
    return closer-1


if __name__ == "__main__":
    print('D14P1 result:', d14p1())
    print('D14P2 result:', d14p2())
