import heapq
import math
import time

MOVES = ['Up', 'Down', 'Left', 'Right']

def heuristic(state, goal_state):
    size = int(math.sqrt(len(state)))
    total_distance = 0
    for i, tile in enumerate(state):
        if tile == 0:
            continue  # skip empty tile
        goal_index = goal_state.index(tile)
        x1, y1 = divmod(i, size)
        x2, y2 = divmod(goal_index, size)
        total_distance += abs(x1 - x2) + abs(y1 - y2)
    return total_distance


def get_possible_moves(state):
    size = int(math.sqrt(len(state)))
    zero_index = state.index(0)
    row, col = divmod(zero_index, size)

    moves = []
    if row > 0:
        moves.append("Up")
    if row < size - 1:
        moves.append("Down")
    if col > 0:
        moves.append("Left")
    if col < size - 1:
        moves.append("Right")
    return moves


def apply_move(state, move):
    size = int(math.sqrt(len(state)))
    zero_index = state.index(0)
    row, col = divmod(zero_index, size)
    new_state = list(state)

    if move == "Up":
        swap_index = (row - 1) * size + col
    elif move == "Down":
        swap_index = (row + 1) * size + col
    elif move == "Left":
        swap_index = row * size + (col - 1)
    elif move == "Right":
        swap_index = row * size + (col + 1)
    else:
        return state  # invalid move

    new_state[zero_index], new_state[swap_index] = new_state[swap_index], new_state[zero_index]
    return tuple(new_state)


def reconstruct_path(came_from, current):
    path = []
    while current in came_from:
        current, move = came_from[current]
        path.insert(0, (current, move))
    return path

def a_star(start_state, goal_state):
    start_time = time.perf_counter()

    start = tuple(start_state)
    goal = tuple(goal_state)

    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal), 0, start))  # (f, g, state)

    came_from = {}  # state -> (parent_state, move)
    g_score = {start: 0}

    while open_set:
        _, g, current = heapq.heappop(open_set)

        if current == goal:
            elapsed_time = time.perf_counter() - start_time
            return reconstruct_path(came_from, current), elapsed_time

        for move in get_possible_moves(current):
            neighbor = apply_move(current, move)
            tentative_g_score = g + 1
    
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = (current, move)
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score, tentative_g_score, neighbor))

    return None , 0.0
