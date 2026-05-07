<p align="center">
  <img src="assets/tmux-jump-logo.png"
       alt="Vimium/Easymotion like cursor jump for tmux."
       title="tmux-jump" />
</p>

# tmux-jump (Python Fork)

[中文文档 (Chinese)](README.zh-hans.md)

`tmux-jump` is a tmux plugin inspired by Vimium/Easymotion. It allows you to move the cursor quickly across the terminal screen by entering simple key sequences.

**This is a Python-based fork of [schasse/tmux-jump](https://github.com/schasse/tmux-jump)**. Unlike the original, this version removes the Ruby dependency and is rewritten in Python 3 using only the standard library, making it ideal for servers where Ruby might not be available.

![tmux-jump-demo](https://user-images.githubusercontent.com/3882305/74186577-2f6aad80-4c4b-11ea-8054-91c54e3dd2af.gif)

## Key Changes

1.  **Language Migration**: Core logic ported from Ruby 2.3+ to Python 3.6+.
2.  **Zero Dependencies**: Runtime only requires Python standard libraries; no third-party packages needed.
3.  **Compatibility Improvements**: Implements a "dual-mode" approach (Strings for logic, Bytes for rendering) to ensure ANSI escape sequences are handled correctly across different terminals.

## Requirements

* [tmux](https://github.com/tmux/tmux) >= 3.1
* [python](https://www.python.org/) >= 3.6

## Installation via [TPM](https://github.com/tmux-plugins/tpm)

Add the following to your `~/.tmux.conf`:

```
set -g @plugin 'douo/tmux-jump-py'
```
Press <kbd>tmux-prefix</kbd> + <kbd>I</kbd> to fetch and activate the plugin.

## Manual Installation

Clone the repository:

```
git clone https://github.com/douo/tmux-jump-py ~/.tmux-jump-py
```

Add the following to `.tmux.conf`:

```
run-shell ~/.tmux-jump-py/tmux-jump.tmux
```

Reload tmux:

```
tmux source-file ~/.tmux.conf
```

## Usage

* Press <kbd>tmux-prefix</kbd> + <kbd>j</kbd> (or your custom key) and enter the first character of the target word.
* The screen will render and highlight keys for each matching word.
* Type the key sequence shown over the target word to jump.
* The cursor will move to that word in copy mode.

## Customization

You can customize the key binding in your `.tmux.conf`:

```
set -g @jump-key 's'
```

Customize foreground and background colors (using ANSI codes):
```
set -g @jump-bg-color '\x1b[0m\x1b[90m'
set -g @jump-fg-color '\x1b[1m\x1b[31m'
```

Change key position:
```
# Keys overlap with the word (default)
set -g @jump-keys-position 'left'

# Keys appear to the left of the word without overlap
set -g @jump-keys-position 'off_left'
```

## Similar Projects

* [schasse/tmux-jump](https://github.com/schasse/tmux-jump) (Original Ruby Version)
* [vimium](https://vimium.github.io/)
* [easymotion](https://github.com/easymotion/vim-easymotion)
