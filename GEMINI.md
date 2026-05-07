# tmux-jump

`tmux-jump` 是一个受 Vimium/Easymotion 启发的 tmux 插件，旨在通过简单的按键序列快速在终端窗口中移动光标，而无需使用鼠标。

## 项目概览

- **主要语言**: Python (核心逻辑), Bash (胶水脚本)
- **核心功能**: 捕获 tmux 面板内容，高亮目标单词的跳转键，并在选择后自动移动光标。
- **依赖**: 
    - `tmux` >= 3.1
    - `python` >= 3.6

## 项目结构

- `tmux-jump.tmux`: 插件入口，负责在 tmux 中绑定快捷键。
- `scripts/`:
    - `tmux_jump.py`: 核心跳转逻辑实现，包含屏幕捕获、单词定位、UI 渲染和光标移动。
    - `tmux-jump.sh`: Bash 包装脚本，负责初始化环境并调用 Python 脚本。
    - `utils.sh`: 辅助 shell 函数，用于获取 tmux 配置选项。
- `tests/`: 包含使用 Python `unittest` 编写的单元测试。
- `assets/`: 包含项目图标和演示动画。

## 开发与运行

### 安装
可通过 [TPM (Tmux Plugin Manager)](https://github.com/tmux-plugins/tpm) 安装：
```tmux
set -g @plugin 'schasse/tmux-jump'
```

### 运行
默认快捷键为 `prefix + j`。按下后输入一个字符，插件会标记所有以该字符开头的单词位置，再次输入显示的跳转键即可跳转。

### 测试
项目使用 Python `unittest` 进行测试。运行测试命令：
```bash
python3 tests/test_tmux_jump.py
```

## 配置项 (tmux.conf)

- `@jump-key`: 触发快捷键 (默认: 'j')
- `@jump-bg-color`: 背景颜色 (ANSI 转义码)
- `@jump-fg-color`: 前景颜色 (ANSI 转义码)
- `@jump-keys-position`: 跳转键显示位置 ('left' 或 'off_left')

## 开发规范

- **Python**: 遵循 PEP 8 编程规范，仅使用标准库以保持零依赖。
- **Tmux 插件**: 遵循 tmux 插件的标准结构，通过 `.tmux` 文件进行集成。
- **测试**: 使用 `unittest` 编写测试，确保核心逻辑的稳定性。
