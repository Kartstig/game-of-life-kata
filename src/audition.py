#!/usr/bin/python
import converter, file_tools


START_FILE = 'start.txt'

def format_output(state: list, bounds: tuple, generation: int) -> str:
    """Convert binary state to ascii output"""
    result = f'Generation {generation}:\n{bounds[0]} {bounds[1]}\n'
    for j in range(0, bounds[1]):
        for i in range(0, bounds[0]):
            result += converter.bin2ascii(state[j][i])
        result += '\n'
    return result

def get_neighbors(point: tuple, bounds: tuple) -> list:
    """
    Calculate all possible neighbor points given a starting point.
    Doesn't include starting point or out of bounds points.
    """
    return [ (x, y) for x in range(point[0]-1, point[0]+2) \
        for y in range(point[1]-1, point[1]+2) \
            if 0 <= point[0] < bounds[0] and \
                0 <= point[1] < bounds[1] and \
                (x != point[0] or y != point[1]) and \
                0 <= x < bounds[0] and \
                0 <= y < bounds[1]
    ]

def get_neighbors_count(game_state: list, neighbors: list) -> int:
    """Count how many neighbors are alive"""
    states = [ game_state[j][i] for i, j in neighbors ]
    return sum(states)

def get_new_state(current_state: int, neighbor_count: int) -> int:
    """Conway algorithim for new state"""
    if neighbor_count < 2 and current_state:
        return 0
    elif 2 <= neighbor_count <= 3 and current_state:
        return 1
    elif neighbor_count > 3 and current_state:
        return 0
    elif neighbor_count == 3 and not current_state:
        return 1
    else:
        return current_state

def main():
    generation = 1
    bounds = file_tools.get_bounds(START_FILE)
    game_state = file_tools.get_game_state(START_FILE, bounds)
    new_state, generation = next_generation(game_state, bounds, generation)
    output = format_output(new_state, bounds, generation)
    print(output)
    return True

def next_generation(game_state: list, bounds: tuple, generation: int) -> list:
    """
    Calculate the next generation based on current
    game state and boundary conditions
    """
    result = []
    for j in range(0, bounds[1]):
        result.append([])
        for i in range(0, bounds[0]):
            neighbors = get_neighbors((i, j), bounds)
            alive_neighbors = get_neighbors_count(game_state, neighbors)
            result[j] += [get_new_state(game_state[j][i], alive_neighbors)]
    return result, generation+1

if __name__ == "__main__":
    main()
