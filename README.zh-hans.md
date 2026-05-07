<p align="center">
  <img src="assets/tmux-jump-logo.png"
       alt="Vimium/Easymotion 风格的 tmux 光标跳转工具。"
       title="tmux-jump" />
</p>

# tmux-jump (Python 移植版)

[English Version](README.md)

`tmux-jump` 是一个受 Vimium/Easymotion 启发的 tmux 插件。它允许你通过简单的按键序列在终端屏幕上快速移动光标。

**本项目是 [schasse/tmux-jump](https://github.com/schasse/tmux-jump) 的 Python 移植版本**。与原版不同，此版本移除了对 Ruby 的依赖，改用 Python 3 (仅使用标准库) 重新实现，非常适合在未安装 Ruby 的服务器环境中使用。

![tmux-jump-demo](https://user-images.githubusercontent.com/3882305/74186577-2f6aad80-4c4b-11ea-8054-91c54e3dd2af.gif)

## 主要改进

1.  **语言迁移**: 核心逻辑从 Ruby 2.3+ 移植到了 Python 3.6+。
2.  **零依赖**: 运行时仅依赖 Python 标准库，无需安装任何第三方包。
3.  **兼容性优化**: 采用“双模式”处理方案（逻辑层用字符串，渲染层用字节流），确保在不同终端下都能正确处理 ANSI 转义序列。

## 依赖要求

* [tmux](https://github.com/tmux/tmux) >= 3.1
* [python](https://www.python.org/) >= 3.6

## 通过 [TPM](https://github.com/tmux-plugins/tpm) 安装

在你的 `~/.tmux.conf` 中添加以下内容：

```
set -g @plugin 'douo/tmux-jump-py'
```
按下 <kbd>tmux-prefix</kbd> + <kbd>I</kbd> 来拉取并激活插件。

## 手动安装

克隆仓库：

```
git clone https://github.com/douo/tmux-jump-py ~/.tmux-jump-py
```

在 `.tmux.conf` 中添加：

```
run-shell ~/.tmux-jump-py/tmux-jump.tmux
```

重新加载 tmux：

```
tmux source-file ~/.tmux.conf
```

## 使用方法

* 按下 <kbd>tmux-prefix</kbd> + <kbd>j</kbd> (或你自定义的快捷键) 并输入目标单词的首字母。
* 屏幕会重新渲染，并为每个匹配的单词高亮显示跳转键。
* 输入目标单词上显示的按键序列即可完成跳转。
* 跳转后，光标将移动到该单词位置，并进入 tmux 的复制模式 (copy mode)。

## 自定义配置

你可以在 `.tmux.conf` 中自定义快捷键：

```
set -g @jump-key 's'
```

自定义前景和背景颜色 (使用 ANSI 转义码)：
```
set -g @jump-bg-color '\x1b[0m\x1b[90m'
set -g @jump-fg-color '\x1b[1m\x1b[31m'
```

更改按键显示位置：
```
# 按键与单词重叠（默认）
set -g @jump-keys-position 'left'

# 按键显示在单词左侧，不重叠
set -g @jump-keys-position 'off_left'
```

## 相关项目

* [schasse/tmux-jump](https://github.com/schasse/tmux-jump) (原始 Ruby 版本)
* [vimium](https://vimium.github.io/)
* [easymotion](https://github.com/easymotion/vim-easymotion)
