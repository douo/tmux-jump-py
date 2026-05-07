import unittest
from unittest.mock import MagicMock, patch
import os
import sys

# Add scripts to path so we can import tmux_jump
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))
import tmux_jump as tj

class TestTmuxJump(unittest.TestCase):
    def setUp(self):
        tj.Config.pane_nr = '%68'
        tj.Config.pane_mode = '0'
        tj.Config.pane_tty_file = '/dev/null' # Mock TTY
        
        self.simple_screen = (
            "~$ echo 'hello world! easymotion for tmux :)'\n"
            "hello world! easymotion for tmux :)\n"
            "~$"
        )
        
        line = "~$ echo 'eello eorld! easymotion eor emux :)'\n"
        self.many_es_screen = (line * 9).strip()

    def test_positions_of(self):
        self.assertEqual(tj.positions_of('h', self.simple_screen), [9, 46])
        self.assertEqual(tj.positions_of('e', self.simple_screen), [3, 22, 59])
        self.assertEqual(tj.positions_of('s', self.simple_screen), [])

    def test_keys_for(self):
        keys_size = len(tj.KEYS)
        # Test cases: [position_count, expected_total_size, expected_key_len]
        test_cases = [
            [1, keys_size, 1],
            [keys_size - 1, keys_size, 1],
            [keys_size, keys_size, 1],
            [keys_size + 1, keys_size**2, 2],
            [keys_size**2 - 1, keys_size**2, 2],
            [keys_size**2, keys_size**2, 2],
            [keys_size**2 + 1, keys_size**3, 3],
        ]
        
        for pos_count, expected_size, expected_len in test_cases:
            calculated_keys = tj.keys_for(pos_count)
            self.assertEqual(len(calculated_keys), expected_size)
            self.assertEqual(len(calculated_keys[0]), expected_len)

    @patch('tmux_jump.prompt_char')
    @patch('tmux_jump.draw_keys_onto_tty')
    def test_prompt_position_index_no_match(self, mock_draw, mock_prompt):
        mock_prompt.return_value = 'b'
        self.assertIsNone(tj.prompt_position_index([3, 22, 59], self.simple_screen))

    @patch('tmux_jump.prompt_char')
    @patch('tmux_jump.draw_keys_onto_tty')
    def test_prompt_position_index_cancel(self, mock_draw, mock_prompt):
        mock_prompt.return_value = None
        self.assertIsNone(tj.prompt_position_index([3, 22, 59], self.simple_screen))

    def test_prompt_position_index_single(self):
        self.assertEqual(tj.prompt_position_index([100], self.simple_screen), 0)

    @patch('tmux_jump.prompt_char')
    @patch('tmux_jump.draw_keys_onto_tty')
    def test_prompt_position_index_many(self, mock_draw, mock_prompt):
        mock_prompt.return_value = 'j'
        positions = list(range(82))
        self.assertEqual(tj.prompt_position_index(positions, self.many_es_screen), 0)

if __name__ == '__main__':
    unittest.main()
