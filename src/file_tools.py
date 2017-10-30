#!/usr/bin/python
import converter


def get_bounds(file: str) -> tuple:
    """Read boundary conditions from file"""
    raw_bounds, = _get_lines(file, 1, 1)
    return _parse_line_bounds(raw_bounds)

def get_game_state(file: str, bounds: tuple) -> list:
    """Read state from file"""
    raw_state = _get_lines(file, 2, bounds[1]+2)
    return _parse_line_states(raw_state, bounds[0])

def _get_lines(filename: str, start: int=0, end: int=None) -> list:
    """Read line(s) from a file"""
    result = []
    with open(filename, 'r') as f:
        for idx, line in enumerate(f):
            if idx >= start and (idx <= end if end else True):
                result.append(line)
    return result

def _parse_line_bounds(line: str) -> tuple:
    """Parse a boundary definition from text"""
    y, x = tuple(int(val) for val in line.split())
    return (x, y)

def _parse_line_state(line: str, row_len: int) -> list:
    """Pares a game state definition from text"""
    stripped = line.strip()
    return [ converter.ascii2bin(stripped[idx]) for idx in range(0, row_len) ]

def _parse_line_states(raw_states: list, row_len: int) -> list:
    return [ _parse_line_state(line, row_len) for line in raw_states ]