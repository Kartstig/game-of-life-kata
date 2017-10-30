import os
import sys
import unittest
from unittest.mock import Mock, patch

# Import application code here ...
sys.path.append(os.path.join(os.getcwd(), 'src'))
import converter, file_tools, audition


class TestAudition(unittest.TestCase):

    @patch('file_tools.get_bounds')
    @patch('file_tools.get_game_state')
    @patch('audition.next_generation', return_value=[Mock(), Mock()])
    @patch('audition.format_output')
    def test_main_ok(self, format_output, next_generation, get_game_state, get_bounds):
        res = audition.main()

        get_bounds.assert_called_with(audition.START_FILE)
        get_game_state.assert_called_with(
            audition.START_FILE,
            get_bounds.return_value
        )
        next_generation.assert_called_with(
            get_game_state.return_value,
            get_bounds.return_value,
            1
        )
        audition.format_output.assert_called_with(
            next_generation.return_value[0],
            get_bounds.return_value,
            next_generation.return_value[1]
        )
        assert res == True

    def test_next_generation(self):
        test_cases = [
            (([[0,0,0]], (3,1), 1), ([[0,0,0]], 2)),
            (([[0,0,0],
               [1,1,1],
               [0,0,0]], (3,3), 1),
            ([[0,1,0],
              [0,1,0],
              [0,1,0]], 2)), # Blinker
            (([[0,0,0,0],
               [0,1,1,0],
               [0,1,1,0],
               [0,0,0,0]], (4,4), 1),
            ([[0,0,0,0],
              [0,1,1,0],
              [0,1,1,0],
              [0,0,0,0]], 2)), # Block
        ]
        for test_case in test_cases:
            assert audition.next_generation(*test_case[0]) == test_case[1]

    def test_get_neighbors_ok(self):
        test_cases = [
            (((0,0), (5,5)), [(1,0),(1,1),(0,1)]),
            (((1,1), (5,5)), [(0,0),(1,0),(2,0),(0,1),(2,1),(0,2),(1,2),(2,2)]),
            (((5,5), (6,6)), [(4,5),(4,4),(5,4)])
        ]
        for test_case in test_cases:
            res = audition.get_neighbors(*test_case[0])
            assert set(res) == set(test_case[1])

    def test_get_new_state(self):
        test_cases = [
            ((0, 1), 0),
            ((0, 2), 0),
            ((0, 3), 1),
            ((0, 4), 0),
            ((0, 1), 0),
            ((1, 1), 0),
            ((1, 2), 1),
            ((1, 3), 1),
            ((1, 4), 0)
        ]
        for test_case in test_cases:
            assert audition.get_new_state(*test_case[0]) == test_case[1]

class TestConverter(unittest.TestCase):
    
    def test_ascii2bin_ok(self):
        test_cases = [
            (converter.ASCII_DEAD, 0),
            (converter.ASCII_ALIVE, 1)
        ]
        for test_values in test_cases:
            assert converter.ascii2bin(test_values[0]) == test_values[1]

    def test_ascii2bin_bad(self):
        with self.assertRaises(ValueError):
            converter.ascii2bin('-')

class TestFileTools(unittest.TestCase):

    @patch('file_tools._get_lines', return_value=[Mock()])
    @patch('file_tools._parse_line_bounds')
    def test_get_bounds_ok(self, _parse_line_bounds, _get_lines):
        file = Mock()

        res = file_tools.get_bounds(file)

        _get_lines.assert_called_with(file, 1, 1)
        _parse_line_bounds.assert_called_with(_get_lines.return_value[0])
        assert res == _parse_line_bounds.return_value

    @patch('file_tools._get_lines')
    @patch('file_tools._parse_line_states')
    def test_get_game_state_ok(self, _parse_line_states, _get_lines):
        file = Mock()
        bounds = (4, 4)

        res = file_tools.get_game_state(file, bounds)

        _get_lines.assert_called_with(file, 2, bounds[1]+2)
        _parse_line_states.assert_called_with(
            _get_lines.return_value,
            bounds[0]
        )
        assert res == _parse_line_states.return_value


if __name__ == '__main__':
    unittest.main()
