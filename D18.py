from dijkstra import dijkstra

with open('input/d18.txt') as f:
    d18_input = [list(l.strip()) for l in f.readlines()]


def d18p1():
    grid = d18_input.copy()
    grid[40][40] = '@1'

    return dijkstra(grid)


def d18p2():
    grid = d18_input.copy()
    grid[40][40] = '#'
    grid[39][40] = '#'
    grid[40][39] = '#'
    grid[40][41] = '#'
    grid[41][40] = '#'
    grid[39][39] = '@1'
    grid[41][41] = '@2'
    grid[39][41] = '@3'
    grid[41][39] = '@4'

    return dijkstra(grid)


if __name__ == "__main__":
    print('D18P1 result:', d18p1())
    print('D18P2 result:', d18p2())
