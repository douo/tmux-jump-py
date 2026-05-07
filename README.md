<p align="center">
  <img src="assets/tmux-jump-logo.png"
       alt="Vimium/Easymotion like cursor jump for tmux."
       title="tmux-jump" />
</p>

[![Build Status](https://travis-ci.org/schasse/tmux-jump.svg?branch=master)](https://travis-ci.org/schasse/tmux-jump)

# tmux-jump (Python Fork)

`tmux-jump` 是一个受 Vimium/Easymotion 启发的 tmux 插件，旨在通过简单的按键序列快速在终端窗口中移动光标。

**本项目是 [schasse/tmux-jump](https://github.com/schasse/tmux-jump) 的 Python 移植版本**。相比原版，它移除了对 Ruby 的依赖，改用 Python 3 (标准库) 重新实现，更适合在仅有 Python 环境的服务器上部署。

![tmux-jump-demo](https://user-images.githubusercontent.com/3882305/74186577-2f6aad80-4c4b-11ea-8054-91c54e3dd2af.gif)

## 主要修改

1.  **语言迁移**: 核心逻辑从 Ruby 2.3+ 迁移到 Python 3.6+。
2.  **零依赖**: 运行时仅依赖 Python 标准库，无需安装任何第三方包。
3.  **兼容性优化**: 采用逻辑(String)/渲染(Bytes)双模式处理，解决部分终端 ANSI 转义字符显示问题。

## Requirements

* [tmux](https://github.com/tmux/tmux) >= 3.1
* [python](https://www.python.org/) >= 3.6

## Installation via [TPM](https://github.com/tmux-plugins/tpm)

在 `~/.tmux.conf` 中添加：

```
set -g @plugin 'douo/tmux-jump-py'
```
按下 <kbd>tmux-prefix</kbd> + <kbd>I</kbd> 拉取并生效。
Hit <kbd>tmux-prefix</kbd> + <kbd>I</kbd> to fetch the plugin and source it. You should now be able to use the plugin.

## Manual Installation

Clone the repository:

```
git clone https://github.com/schasse/tmux-jump ~/.tmux-jump
```

Add the following to `.tmux.conf`:

```
run-shell ~/.tmux-jump/tmux-jump.tmux
```

Reload tmux:

```
tmux source-file ~/.tmux.conf
```

## Usage

* <kbd>tmux-prefix</kbd> + <kbd>j</kbd> and enter the first character of a word.
* The screen will rerender and highlight the keys to press to jump to the word.
* Type the key sequence of the word to jump to.
* The cursor moves to the word.

tmux-jump can also be used in in any program and during copy mode.

You can customize the key binding in your `.tmux.conf`:

```
set -g @jump-key 's'
```

You can also customize foreground and background color:
```
set -g @jump-bg-color '\e[0m\e[90m'
set -g @jump-fg-color '\e[1m\e[31m'
```

And the keys position:
```
# keys will overlap with the word (default)
set -g @jump-keys-position 'left'

# keys will be at the left of the word without overlap
set -g @jump-keys-position 'off_left'
```

## Similar Projects

* [vimium](https://vimium.github.io/)
* [easymotion](https://github.com/easymotion/vim-easymotion)
* [ace-jump-mode](https://github.com/winterTTr/ace-jump-mode)
