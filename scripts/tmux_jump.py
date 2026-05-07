import os
import sys
import subprocess
import threading
import queue
import tempfile
import time
from typing import List, Optional, Tuple

# SPECIAL STRINGS
GRAY = os.environ.get('JUMP_BACKGROUND_COLOR', '\x1b[0m\x1b[32m').replace('\\e', '\x1b').encode('utf-8')
RED = os.environ.get('JUMP_FOREGROUND_COLOR', '\x1b[1m\x1b[31m').replace('\\e', '\x1b').encode('utf-8')
CLEAR_SEQ = b'\x1b[2J'
HOME_SEQ = b'\x1b[H'
RESET_COLORS = b'\x1b[0m'
ENTER_ALTERNATE_SCREEN = b'\x1b[?1049h'
RESTORE_NORMAL_SCREEN = b'\x1b[?1049l'

# CONFIG
KEYS_POSITION = os.environ.get('JUMP_KEYS_POSITION', 'left')
KEYS = list('jfhgkdlsa')

class Config:
    pane_nr: str = ""
    pane_tty_file: str = ""
    pane_mode: str = ""
    cursor_y: int = 0
    cursor_x: int = 0
    alternate_on: str = ""
    scroll_position: int = 0
    pane_height: int = 0
    tmp_file: str = ""

def recover_screen_after(func):
    def wrapper(*args, **kwargs):
        if Config.alternate_on == '1':
            return recover_alternate_screen_after(func)(*args, **kwargs)
        else:
            return recover_normal_screen_after(func)(*args, **kwargs)
    return wrapper

def recover_normal_screen_after(func):
    def wrapper(*args, **kwargs):
        with open(Config.pane_tty_file, 'ab') as tty:
            tty.write(ENTER_ALTERNATE_SCREEN + HOME_SEQ)
        
        try:
            returns = func(*args, **kwargs)
        except Exception:
            returns = None
        
        with open(Config.pane_tty_file, 'ab') as tty:
            tty.write(RESTORE_NORMAL_SCREEN)
        return returns
    return wrapper

def recover_alternate_screen_after(func):
    def wrapper(*args, **kwargs):
        # Capture screen with colors
        saved_screen = subprocess.check_output(['tmux', 'capture-pane', '-ep', '-t', Config.pane_nr])
        if saved_screen.endswith(b'\n'):
            saved_screen = saved_screen[:-1]
        saved_screen = saved_screen.replace(b'\n', b'\n\r')

        with open(Config.pane_tty_file, 'ab') as tty:
            tty.write(CLEAR_SEQ + HOME_SEQ)
        
        try:
            returns = func(*args, **kwargs)
        except Exception:
            returns = None
        
        with open(Config.pane_tty_file, 'ab') as tty:
            tty.write(RESET_COLORS + CLEAR_SEQ)
            tty.write(saved_screen)
            # Move cursor back
            cursor_pos = f'\x1b[{Config.cursor_y + 1};{Config.cursor_x + 1}H'.encode('utf-8')
            tty.write(cursor_pos)
            tty.write(RESET_COLORS)
        return returns
    return wrapper

def prompt_char() -> Optional[str]:
    with tempfile.NamedTemporaryFile(prefix="tmux-jump-py") as tmp:
        tmp_path = tmp.name
        subprocess.run(['tmux', 'command-prompt', '-1', '-p', 'char:', 
                        f"run-shell \"printf '%1' >> {tmp_path}\""])
        
        res_queue = queue.Queue()
        
        def read_char():
            start_time = time.time()
            while time.time() - start_time < 10:
                if os.path.exists(tmp_path) and os.path.getsize(tmp_path) > 0:
                    with open(tmp_path, 'r') as f:
                        char = f.read(1)
                        if char:
                            res_queue.put(char)
                            return
                time.sleep(0.05)
            res_queue.put(None)

        def detect_escape():
            last_activity = subprocess.check_output(['tmux', 'display-message', '-p', '#{session_activity}']).strip()
            while True:
                new_activity = subprocess.check_output(['tmux', 'display-message', '-p', '#{session_activity}']).strip()
                if last_activity != new_activity:
                    res_queue.put(None)
                    return
                time.sleep(0.05)

        t1 = threading.Thread(target=read_char, daemon=True)
        t2 = threading.Thread(target=detect_escape, daemon=True)
        t1.start()
        t2.start()
        
        return res_queue.get()

def read_char_from_file(file_path: str) -> Optional[str]:
    start_time = time.time()
    while time.time() - start_time < 10:
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            with open(file_path, 'r') as f:
                char = f.read(1)
                if char:
                    return char
        time.sleep(0.05)
    return None

def positions_of(jump_to_char: str, screen_chars: str) -> List[int]:
    positions = []
    if not screen_chars:
        return positions
    
    jump_to_char = jump_to_char.lower()
    
    # Check first character
    if screen_chars[0].isalnum() and screen_chars[0].lower() == jump_to_char:
        positions.append(0)
        
    for i in range(len(screen_chars) - 1):
        char = screen_chars[i]
        next_char = screen_chars[i+1]
        if not char.isalnum() and next_char.lower() == jump_to_char:
            positions.append(i + 1)
    return positions

def keys_for(position_count: int, current_keys: List[str] = KEYS) -> List[str]:
    if position_count > len(current_keys):
        new_keys = []
        for k in current_keys:
            for next_k in KEYS:
                new_keys.append(k + next_k)
        return keys_for(position_count, new_keys)
    return current_keys

def draw_keys_onto_tty(screen_chars: str, positions: List[int], keys: List[str], key_len: int):
    with open(Config.pane_tty_file, 'ab') as tty:
        cursor = 0
        for i, pos in enumerate(positions):
            # Text before the jump key
            before = screen_chars[cursor:pos].replace('\n', '\n\r').encode('utf-8')
            tty.write(GRAY + before)
            # The jump key itself
            tty.write(RED + keys[i].encode('utf-8'))
            # Advance cursor
            if KEYS_POSITION == 'off_left':
                cursor = pos
            else:
                cursor = pos + key_len
        
        # Remaining text
        after = screen_chars[cursor:].replace('\n', '\n\r').encode('utf-8')
        tty.write(GRAY + after)
        tty.write(HOME_SEQ)

@recover_screen_after
def prompt_position_index(positions: List[int], screen_chars: str) -> Optional[int]:
    if not positions:
        return None
    if len(positions) == 1:
        return 0
    
    keys = keys_for(len(positions))
    key_len = len(keys[0])
    
    draw_keys_onto_tty(screen_chars, positions, keys, key_len)
    
    input_char = prompt_char()
    if input_char is None:
        return None
        
    try:
        key_index = KEYS.index(input_char)
    except ValueError:
        return None
        
    if key_len > 1:
        magnitude = len(KEYS) ** (key_len - 1)
        range_start = key_index * magnitude
        range_end = range_start + magnitude
        remaining_positions = positions[range_start:range_end]
        
        if not remaining_positions:
            return None
            
        lower_index = prompt_position_index(remaining_positions, screen_chars)
        if lower_index is None:
            return None
        return range_start + lower_index
    else:
        return key_index

def main():
    jump_to_char = read_char_from_file(Config.tmp_file)
    if not jump_to_char:
        sys.exit(0)
    
    if Config.pane_mode == '1':
        subprocess.run(['tmux', 'send-keys', '-X', '-t', Config.pane_nr, 'cancel'])
        
    start = -Config.scroll_position
    end = -Config.scroll_position + Config.pane_height - 1
    
    # Capture pane without colors for logic
    screen_chars = subprocess.check_output([
        'tmux', 'capture-pane', '-p', '-t', Config.pane_nr, '-S', str(start), '-E', str(end)
    ]).decode('utf-8', errors='ignore')
    if screen_chars.endswith('\n'):
        screen_chars = screen_chars[:-1]
    
    positions = positions_of(jump_to_char, screen_chars)
    
    # This call is decorated with recover_screen_after
    pos_index = prompt_position_index(positions, screen_chars)
    
    if pos_index is None:
        sys.exit(0)
        
    jump_to = positions[pos_index]
    
    # Execute the jump in tmux
    subprocess.run(['tmux', 'copy-mode', '-t', Config.pane_nr])
    # Handle tmux weirdness
    subprocess.run(['tmux', 'send-keys', '-X', '-t', Config.pane_nr, 'start-of-line'])
    subprocess.run(['tmux', 'send-keys', '-X', '-t', Config.pane_nr, 'top-line'])
    subprocess.run(['tmux', 'send-keys', '-X', '-t', Config.pane_nr, '-N', '200', 'cursor-right'])
    
    subprocess.run(['tmux', 'send-keys', '-X', '-t', Config.pane_nr, 'start-of-line'])
    subprocess.run(['tmux', 'send-keys', '-X', '-t', Config.pane_nr, 'top-line'])
    subprocess.run(['tmux', 'send-keys', '-X', '-t', Config.pane_nr, '-N', str(Config.scroll_position), 'cursor-up'])
    subprocess.run(['tmux', 'send-keys', '-X', '-t', Config.pane_nr, '-N', str(jump_to), 'cursor-right'])

def to_i(s: str) -> int:
    try:
        return int(s)
    except (ValueError, TypeError):
        return 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
        
    Config.pane_nr = subprocess.check_output(['tmux', 'display-message', '-p', '#{pane_id}']).decode('utf-8').strip()
    fmt = '#{pane_id};#{pane_tty};#{pane_in_mode};#{cursor_y};#{cursor_x};#{alternate_on};#{scroll_position};#{pane_height}'
    tmux_data = subprocess.check_output(['tmux', 'display-message', '-p', '-t', Config.pane_nr, '-F', fmt]).decode('utf-8').strip().split(';')
    
    Config.pane_tty_file = tmux_data[1]
    Config.pane_mode = tmux_data[2]
    Config.cursor_y = to_i(tmux_data[3])
    Config.cursor_x = to_i(tmux_data[4])
    Config.alternate_on = tmux_data[5]
    Config.scroll_position = to_i(tmux_data[6])
    Config.pane_height = to_i(tmux_data[7])
    Config.tmp_file = sys.argv[1]
    
    main()
