from utils import *
import heapq

def biastar(draw, grid, start, end):
    idx = 0
    open_set = [[], []]
    heapq.heappush(open_set[idx], (0, start))
    heapq.heappush(open_set[idx ^ 1], (0, end))
    came_from = [{}, {}]
    g_score = [{spot: float("inf") for row in grid for spot in row},
               {spot: float("inf") for row in grid for spot in row}]
    g_score[idx][start] = g_score[idx ^ 1][end] = 0
    f_score = [{spot: float("inf") for row in grid for spot in row},
               {spot: float("inf") for row in grid for spot in row}]
    f_score[idx][start] = f_score[idx ^ 1][end] = h(start.get_pos(), end.get_pos())

    open_set_hash = [{start}, {end}]

    pause = 0
    while len(open_set[0]) and len(open_set[1]):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                bye()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause ^= 1
                elif event.key == pygame.K_q:
                    bye()
        if pause: continue
        if len(open_set[idx]) > len(open_set[idx ^ 1]): idx ^= 1
        current = heapq.heappop(open_set[idx])[1]
        open_set_hash[idx].remove(current)

        if current in open_set_hash[idx ^ 1]:
            print(current.row, current.col)
            reconstruct_path(came_from[0], current, draw)
            reconstruct_path(came_from[1], current, draw)
            # end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[idx][current] + (
                1 if neighbor.row == current.row or neighbor.col == current.col else math.sqrt(2))
            if neighbor.cost_idx: temp_g_score += EXTRA_COST[neighbor.cost_idx]
            if temp_g_score < g_score[idx][neighbor]:
                came_from[idx][neighbor] = current
                g_score[idx][neighbor] = temp_g_score
                f_score[idx][neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash[idx]:
                    heapq.heappush(open_set[idx], (f_score[idx][neighbor], neighbor))
                    open_set_hash[idx].add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start and current != end:
            current.make_closed()

    return False