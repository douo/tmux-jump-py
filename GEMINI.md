# tmux-jump

`tmux-jump` is a tmux plugin inspired by Vimium/Easymotion, designed to move the cursor quickly across the terminal window using simple key sequences without a mouse.

## Project Overview

- **Primary Language**: Python (Core logic), Bash (Glue scripts)
- **Core Functionality**: Capture tmux pane content, highlight jump keys for target words, and move the cursor automatically upon selection.
- **Dependencies**: 
    - `tmux` >= 3.1
    - `python` >= 3.6

## Project Structure

- `tmux-jump.tmux`: Plugin entry point, handles key bindings in tmux.
- `scripts/`:
    - `tmux_jump.py`: Core jump logic implementation (screen capture, word positioning, UI rendering, cursor movement).
    - `tmux-jump.sh`: Bash wrapper script (environment initialization and Python script execution).
    - `utils.sh`: Shell utility functions for fetching tmux configuration options.
- `tests/`: Contains unit tests written using Python's `unittest` framework.
- `assets/`: Icons and demo animations.

## Development & Usage

### Installation
Install via [TPM (Tmux Plugin Manager)](https://github.com/tmux-plugins/tpm):
```tmux
set -g @plugin 'douo/tmux-jump-py'
```

### Usage
Default trigger is `prefix + j`. After pressing, enter a character; the plugin marks all words starting with that character. Enter the displayed jump key to move the cursor.

### Testing
Tests use the standard `unittest` framework. Run tests with:
```bash
python3 tests/test_tmux_jump.py
```

## Configuration Options (tmux.conf)

- `@jump-key`: Trigger key (default: 'j')
- `@jump-bg-color`: Background color (ANSI escape code)
- `@jump-fg-color`: Foreground color (ANSI escape code)
- `@jump-keys-position`: Jump key display position ('left' or 'off_left')

## Engineering Standards

- **Python**: Follow PEP 8 guidelines. Use only the standard library for zero-dependency runtime.
- **Tmux Plugin**: Adhere to standard tmux plugin structure and integration via `.tmux` files.
- **Testing**: Maintain high test coverage for core logic using `unittest`.
