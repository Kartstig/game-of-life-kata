#!/usr/bin/python


ASCII_ALIVE = '*'
ASCII_DEAD = '.'

def ascii2bin(value: str) -> int:
    """Convert ascii text to binary"""
    if value == ASCII_ALIVE:
        return 1
    elif value == ASCII_DEAD:
        return 0
    else:
        raise ValueError(f'Invalid ascii value {value}')

def bin2ascii(value: int) -> str:
    """Convert binary to ascii text"""
    if value:
        return ASCII_ALIVE
    else:
        return ASCII_DEAD