# coding: utf-8

from heapq import heappush
from heapq import heappop

F, H, G, POS, OPEN, VALID, PARENT, DISTANCE  = xrange(8)

def astar(start_pos, goal_pos, blocks, bf, distance, start_g=1):
    """
    """

    start_h = bf.heuristic(start_pos, goal_pos)
    start = [start_g + start_h, start_h, start_g, start_pos, True, True, None, 0]
    nodes = {start_pos: start}
    heap = [start]
    best = start

    while heap:
        current = heappop(heap)
        current[OPEN] = False

        if current[POS] == goal_pos or current[DISTANCE] >= distance:
            best = current
            break

        for neighbor_pos in bf.neighbors(current[POS], blocks, goal_pos):
            neighbor_g = current[G] + bf.cost(current[POS], neighbor_pos)
            neighbor = nodes.get(neighbor_pos)

            if neighbor is None:
                # new node
                neighbor_h = bf.heuristic(neighbor_pos, goal_pos)
                neighbor = [neighbor_g + neighbor_h, neighbor_h, neighbor_g,
                            neighbor_pos, True, True, current[POS], current[DISTANCE] + 1]
                nodes[neighbor_pos] = neighbor
                heappush(heap, neighbor)
 
                if neighbor_h < best[H]:
                    best = neighbor

            elif neighbor_g < neighbor[G]:
                # better path

                if neighbor[OPEN]:
                    neighbor[VALID] = False
                    nodes[neighbor_pos] = neighbor = list(neighbor)
                    neighbor[F] = neighbor_g + neighbor[H]
                    neighbor[G] = neighbor_g
                    neighbor[VALID] = True
                    neighbor[PARENT] = current[POS]
                    neighbor[DISTANCE] = current[POS] + 1
                else:
                    neighbor[F] = neighbor_g + neighbor[H]
                    neighbor[G] = neighbor_g
                    neighbor[PARENT] = current[POS]
                    neighbor[DISTANCE] = current[POS] + 1
                    neighbor[OPEN] = True

                heappush(heap, neighbor)

        while heap and not heap[0][VALID]:
            heappop(heap)

    path = []
    current = best

    while not current[PARENT] is None:
        path.append(current[POS])
        current = nodes[current[PARENT]]

    return path
