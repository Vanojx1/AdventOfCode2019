import collections
import heapq


def dijkstra(grid):
    R, C = len(grid), len(grid[0])
    location = {v: (r, c)
                for r, row in enumerate(grid)
                for c, v in enumerate(row)
                if v not in '.#'}

    keys = tuple()
    for k, (r, c) in list(location.items()):
        if '@' in k:
            keys += (k, )

    def neighbors(r, c):
        for cr, cc in ((r-1, c), (r, c-1), (r+1, c), (r, c+1)):
            if 0 <= cr < R and 0 <= cc < C:
                yield cr, cc

    def bfs_from(source):
        r, c = location[source]
        seen = [[False] * C for _ in range(R)]
        seen[r][c] = True
        queue = collections.deque([(r, c, 0)])
        dist = {}
        while queue:
            r, c, d = queue.popleft()
            if source != grid[r][c] != '.':
                dist[grid[r][c]] = d
                continue
            for cr, cc in neighbors(r, c):
                if grid[cr][cc] != '#' and not seen[cr][cc]:
                    seen[cr][cc] = True
                    queue.append((cr, cc, d+1))
        return dist

    dists = {place: bfs_from(place) for place in location}
    target_state = 2 ** sum(p.islower() for p in location) - 1
    pq = [(0, (keys, 0))]
    final_dist = collections.defaultdict(lambda: float('inf'))
    while pq:
        d, node = heapq.heappop(pq)
        if final_dist[node] < d:
            continue
        places, state = node
        if state == target_state:
            return d
        for i, place in enumerate(places):
            for destination, d2 in dists[place].items():
                state2 = state
                if destination.islower():
                    state2 |= (1 << (ord(destination) - ord('a')))
                elif destination.isupper():
                    if not(state & (1 << (ord(destination) - ord('A')))):
                        continue
                next_node = ((places[:i]+(destination,)+places[i+1:], state2))
                if d + d2 < final_dist[next_node]:
                    final_dist[next_node] = d + d2
                    heapq.heappush(pq, (d + d2, next_node))
    return -1
