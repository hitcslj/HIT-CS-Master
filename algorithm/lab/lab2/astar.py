from utils import *
import heapq


def astar(draw, grid, start, end):
    # count = 0
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    pause = 0
    while len(open_set):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                bye()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause ^= 1
                elif event.key == pygame.K_q:
                    bye()

        if pause: continue
        current = heapq.heappop(open_set)[1]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            # end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + (
                1 if neighbor.row == current.row or neighbor.col == current.col else math.sqrt(2))
            if neighbor.cost_idx: temp_g_score += EXTRA_COST[neighbor.cost_idx]
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    # count += 1
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


