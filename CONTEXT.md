# Context: tmux-jump (Python Migration)

`tmux-jump` 是一个 tmux 插件，允许用户通过搜索字符并输入生成的“跳转键”来快速定位光标。

## 术语表 (Glossary)

- **Pane (面板)**: 当前操作的 tmux 终端窗口。插件会捕获其内容并在此之上渲染 UI。
- **Jump Character (跳转字符)**: 用户输入的第一个字符，用于过滤屏幕上以该字符开头的单词。
- **Jump Key (跳转键)**: 插件为匹配到的单词分配的唯一按键序列（如 'f', 'jk'）。
- **Jump Mode (跳转模式)**: 插件的交互状态。在此模式下，原始屏幕内容会被临时覆盖或修改，以显示跳转键。
- **TTY File (TTY 文件)**: tmux 面板对应的设备文件（如 `/dev/pts/1`），插件直接向其写入 ANSI 转义序列以实现无缝渲染。
- **Alternate Screen (备用屏幕)**: 一种终端状态，允许插件在不破坏原始滚动缓冲区的情况下进行绘制。

## 核心决策 (Decisions)

- **处理模式 (Dual-mode Processing)**: 搜索逻辑使用 `str` (UTF-8 字符串)，以利用 Python 的字符串处理能力；UI 渲染和恢复屏幕使用 `bytes` (原始字节流)，以直接处理 `tmux capture-pane -ep` 输出的 ANSI 转义码，避免编解码错误。
- **运行环境 (Runtime Environment)**: 目标为 Python 3.6+。仅使用 Python 标准库（如 `subprocess`, `threading`, `queue`, `unittest`），不引入第三方依赖，以确保在各种服务器环境下的零安装成本。
- **代码规范 (Coding Standards)**: 使用类型提示 (`typing`) 增强代码健壮性，使用 `f-strings` 提高可读性。
