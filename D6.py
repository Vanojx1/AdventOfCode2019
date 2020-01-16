from anytree import Node
# from anytree.exporter import DotExporter

with open('input/d6.txt') as f:
    d6_input = {k: v for v, k in [
        l.rstrip('\n').split(')') for l in f.readlines()]}

objects = set(list(d6_input.values()) + list(d6_input.keys()))


def orbit_chain(obj):
    if obj in d6_input:
        return [obj] + orbit_chain(d6_input[obj])
    else:
        return [obj]


def d6p1():
    total_orbits = 0
    for obj in objects:
        total_orbits += len(orbit_chain(obj))-1
    return total_orbits


def d6p2():
    com_distances = {o: orbit_chain(o) for o in objects}

    rev_san = com_distances['SAN'][::-1]
    rev_you = com_distances['YOU'][::-1]

    last_common = None
    for i, common_o in enumerate(rev_san):
        if common_o != rev_you[i]:
            last_common = rev_you[i-1]
            break

    san_to_common = [o for i, o in enumerate(
        com_distances['SAN']) if i < com_distances['SAN'].index(last_common)]
    del san_to_common[0]
    you_to_common = [o for i, o in enumerate(
        com_distances['YOU']) if i < com_distances['YOU'].index(last_common)]
    del you_to_common[0]

    full_path = san_to_common + [last_common] + you_to_common[::-1]

    tree = {o: Node(o) for o in objects}

    for k, v in d6_input.items():
        tree[k].parent = tree[v]
        if k in ['YOU', 'SAN']:
            tree[k].name = '==> %s <==' % tree[k].name

    # DotExporter(tree['COM']).to_picture('export.jpg')

    return len(full_path) - 1


if __name__ == "__main__":
    print('D6P1 result:', d6p1())
    print('D6P2 result:', d6p2())
