"""
TUI仪表盘模块

使用纯终端ANSI escape codes实现交互式仪表盘界面，
显示扫描进度条、问题分布饼图（ASCII art）、文件热力图，
支持键盘交互（上下选择问题）。
"""

import os
import sys
import select
import termios
import tty
from typing import TYPE_CHECKING, List, Dict, Optional

if TYPE_CHECKING:
    from ..scanner import ScanResult

from ..utils import (
    Colors, colorize, bold, red, green, yellow, blue, cyan,
    magenta, severity_to_color,
)


class TUIChecker:
    """TUI仪表盘检查结果浏览器

    提供交互式终端界面浏览扫描结果，支持键盘上下选择问题。
    """

    def __init__(self, result: "ScanResult"):
        """初始化TUI仪表盘

        Args:
            result: 扫描结果
        """
        self.result = result
        self.selected_index: int = 0
        self.scroll_offset: int = 0
        self.current_tab: int = 0  # 0=问题列表, 1=统计, 2=文件热力图
        self.tab_names: List[str] = ["问题列表", "统计概览", "文件热力图"]
        self._terminal_height: int = 24
        self._terminal_width: int = 80

    def run(self) -> None:
        """运行TUI仪表盘"""
        # 检测终端大小
        self._detect_terminal_size()

        # 显示仪表盘
        self._draw()

        # 键盘交互循环
        if sys.stdin.isatty():
            self._interaction_loop()
        else:
            # 非交互模式，直接显示
            print("\n按 q 退出")

    def _detect_terminal_size(self) -> None:
        """检测终端窗口大小"""
        try:
            size = os.get_terminal_size()
            self._terminal_height = size.lines
            self._terminal_width = size.columns
        except OSError:
            self._terminal_height = 24
            self._terminal_width = 80

    def _draw(self) -> None:
        """绘制整个TUI界面"""
        # 清屏
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()

        # 标题栏
        self._draw_header()

        # 标签栏
        self._draw_tabs()

        # 内容区
        if self.current_tab == 0:
            self._draw_issues_list()
        elif self.current_tab == 1:
            self._draw_statistics()
        elif self.current_tab == 2:
            self._draw_file_heatmap()

        # 底部状态栏
        self._draw_footer()

        sys.stdout.flush()

    def _draw_header(self) -> None:
        """绘制标题栏"""
        title = bold("  PyGuard-CLI 代码质量仪表盘")
        version = colorize("v1.0.0", Colors.DIM)
        padding = self._terminal_width - len("PyGuard-CLI 代码质量仪表盘") - len("v1.0.0") - 4
        padding = max(padding, 0)
        header = f"\033[44;37m{title}{' ' * padding}{version}\033[0m"
        sys.stdout.write(header + "\n")

    def _draw_tabs(self) -> None:
        """绘制标签栏"""
        tab_line = "  "
        for i, name in enumerate(self.tab_names):
            if i == self.current_tab:
                tab_line += colorize(f" [{name}] ", Colors.REVERSE)
            else:
                tab_line += f" {name} "
        sys.stdout.write(tab_line + "\n")
        sys.stdout.write(colorize("  " + "-" * (self._terminal_width - 4), Colors.DIM) + "\n")

    def _draw_issues_list(self) -> None:
        """绘制问题列表"""
        issues = self.result.issues
        if not issues:
            sys.stdout.write(green("\n  未发现问题，代码质量良好!\n"))
            return

        # 可显示的行数
        available_lines = self._terminal_height - 6
        visible_issues = issues[self.scroll_offset:self.scroll_offset + available_lines]

        for i, issue in enumerate(visible_issues):
            real_index = self.scroll_offset + i
            marker = " > " if real_index == self.selected_index else "   "
            color = severity_to_color(issue.severity)
            sym = issue.severity[0].upper()

            line = (
                f"{marker}"
                f"{colorize(f'[{sym}]', color)} "
                f"{bold(issue.rule_id)} "
                f"{issue.file_path.split('/')[-1]}:{issue.line_no} "
                f"{issue.message}"
            )
            # 截断过长的行
            if len(line) > self._terminal_width - 2:
                line = line[:self._terminal_width - 5] + "..."

            if real_index == self.selected_index:
                line = colorize(line, Colors.REVERSE)
            sys.stdout.write(line + "\n")

        # 选中问题的详情
        if 0 <= self.selected_index < len(issues):
            issue = issues[self.selected_index]
            sys.stdout.write(colorize("  " + "-" * (self._terminal_width - 4), Colors.DIM) + "\n")
            sys.stdout.write(f"  {bold('文件:')} {issue.file_path}\n")
            sys.stdout.write(f"  {bold('位置:')} 第{issue.line_no}行, 第{issue.column}列\n")
            sys.stdout.write(f"  {bold('规则:')} {issue.rule_id} ({issue.category})\n")
            sys.stdout.write(f"  {bold('描述:')} {issue.message}\n")
            if issue.suggestion:
                sys.stdout.write(f"  {magenta('建议:')} {issue.suggestion}\n")

    def _draw_statistics(self) -> None:
        """绘制统计概览"""
        result = self.result

        sys.stdout.write("\n")
        sys.stdout.write(bold("  扫描统计\n"))
        sys.stdout.write(colorize("  " + "-" * 40, Colors.DIM) + "\n")
        sys.stdout.write(f"  扫描文件数:   {result.files_scanned}\n")
        sys.stdout.write(f"  问题文件数:   {result.files_with_issues}\n")
        sys.stdout.write(f"  代码总行数:   {result.total_lines}\n")
        sys.stdout.write(f"  扫描耗时:     {result.scan_time:.3f}s\n")
        sys.stdout.write("\n")

        # 问题分布饼图（ASCII art）
        sys.stdout.write(bold("  问题分布\n"))
        self._draw_pie_chart()

        sys.stdout.write("\n")

        # 分类统计柱状图
        sys.stdout.write(bold("  分类统计\n"))
        self._draw_category_chart()

    def _draw_pie_chart(self) -> None:
        """绘制ASCII饼图"""
        total = len(self.result.issues)
        if total == 0:
            sys.stdout.write("  无数据\n")
            return

        error_pct = self.result.error_count / total * 100
        warning_pct = self.result.warning_count / total * 100
        info_pct = self.result.info_count / total * 100

        # 使用ASCII字符绘制简单的水平条形图代替饼图
        bar_width = 40
        error_width = int(bar_width * error_pct / 100)
        warning_width = int(bar_width * warning_pct / 100)
        info_width = bar_width - error_width - warning_width

        bar = (
            f"  {red('#' * error_width)}"
            f"{yellow('#' * warning_width)}"
            f"{cyan('#' * max(info_width, 0))}"
        )
        sys.stdout.write(bar + "\n")
        sys.stdout.write(f"  {red('错误')} {error_pct:.1f}%  "
                         f"{yellow('警告')} {warning_pct:.1f}%  "
                         f"{cyan('信息')} {info_pct:.1f}%\n")

    def _draw_category_chart(self) -> None:
        """绘制分类统计柱状图"""
        category_counts: Dict[str, int] = {}
        category_names = {
            "type": "类型检查",
            "style": "代码风格",
            "security": "安全检测",
            "complexity": "复杂度",
            "performance": "性能",
            "best_practice": "最佳实践",
            "scanner": "扫描错误",
        }

        for issue in self.result.issues:
            cat = issue.category
            category_counts[cat] = category_counts.get(cat, 0) + 1

        if not category_counts:
            sys.stdout.write("  无数据\n")
            return

        max_count = max(category_counts.values())
        bar_max_width = 25

        for cat, count in sorted(category_counts.items(), key=lambda x: -x[1]):
            name = category_names.get(cat, cat)
            bar_len = int(bar_max_width * count / max_count) if max_count > 0 else 0
            bar = colorize("#" * bar_len, Colors.GREEN)
            sys.stdout.write(f"  {name:8s} {bar} {count}\n")

    def _draw_file_heatmap(self) -> None:
        """绘制文件热力图"""
        file_issues: Dict[str, int] = {}
        for issue in self.result.issues:
            fp = issue.file_path
            file_issues[fp] = file_issues.get(fp, 0) + 1

        if not file_issues:
            sys.stdout.write(green("\n  所有文件均无问题!\n"))
            return

        sorted_files = sorted(file_issues.items(), key=lambda x: -x[1])
        max_issues = sorted_files[0][1] if sorted_files else 1

        sys.stdout.write(bold("\n  文件问题热力图\n"))
        sys.stdout.write(colorize("  " + "-" * (self._terminal_width - 4), Colors.DIM) + "\n")

        for file_path, count in sorted_files[:self._terminal_height - 8]:
            short_name = file_path.split("/")[-1]
            intensity = count / max_issues if max_issues > 0 else 0

            # 根据问题数量选择颜色
            if intensity > 0.7:
                color = Colors.BG_RED
            elif intensity > 0.4:
                color = Colors.BG_YELLOW
            elif intensity > 0:
                color = Colors.BG_GREEN
            else:
                color = Colors.RESET

            bar_len = int(30 * intensity)
            bar = colorize(" " * bar_len, color)
            sys.stdout.write(f"  {short_name:30s} {bar} {count}\n")

    def _draw_footer(self) -> None:
        """绘制底部状态栏"""
        total = len(self.result.issues)
        pos = self.selected_index + 1 if total > 0 else 0
        footer = (
            f"\033[44;37m  "
            f"{red(f'错误:{self.result.error_count}')}  "
            f"{yellow(f'警告:{self.result.warning_count}')}  "
            f"{cyan(f'信息:{self.result.info_count}')}  "
            f"{' ' * max(self._terminal_width - 60, 0)}"
            f"↑↓:导航 Tab:切换 q:退出  "
            f"[{pos}/{total}]"
            f"\033[0m"
        )
        sys.stdout.write(footer + "\n")

    def _interaction_loop(self) -> None:
        """键盘交互循环"""
        # 保存终端设置
        try:
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            tty.setraw(fd)
        except (termios.error, OSError):
            # 无法设置raw模式，使用简单输入
            self._simple_interaction()
            return

        try:
            while True:
                # 检查是否有可读输入（非阻塞）
                if select.select([sys.stdin], [], [], 0.1)[0]:
                    ch = sys.stdin.read(1)

                    if ch == "q" or ch == "\x03":  # q 或 Ctrl+C
                        break
                    elif ch == "\x1b":  # ESC序列
                        ch2 = sys.stdin.read(1) if select.select([sys.stdin], [], [], 0.1)[0] else ""
                        if ch2 == "[":
                            ch3 = sys.stdin.read(1) if select.select([sys.stdin], [], [], 0.1)[0] else ""
                            if ch3 == "A":  # 上箭头
                                self._move_up()
                            elif ch3 == "B":  # 下箭头
                                self._move_down()
                    elif ch == "\t":  # Tab
                        self.current_tab = (self.current_tab + 1) % len(self.tab_names)
                        self._draw()
                    elif ch == "j":  # j键下移
                        self._move_down()
                    elif ch == "k":  # k键上移
                        self._move_up()
        finally:
            # 恢复终端设置
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            sys.stdout.write("\033[2J\033[H")  # 清屏
            sys.stdout.write("\033[?25h")  # 显示光标
            sys.stdout.flush()

    def _simple_interaction(self) -> None:
        """简单的交互模式（当无法设置raw终端时）"""
        print("\n  交互模式不可用（非终端环境）")
        print("  使用以下命令查看详情:")
        print("    pyguard scan <path> --format text")
        print("    pyguard scan <path> --format json")
        print("    pyguard scan <path> --format html")

    def _move_up(self) -> None:
        """向上移动选择"""
        if self.selected_index > 0:
            self.selected_index -= 1
            if self.selected_index < self.scroll_offset:
                self.scroll_offset = self.selected_index
            self._draw()

    def _move_down(self) -> None:
        """向下移动选择"""
        if self.selected_index < len(self.result.issues) - 1:
            self.selected_index += 1
            available_lines = self._terminal_height - 6
            if self.selected_index >= self.scroll_offset + available_lines:
                self.scroll_offset = self.selected_index - available_lines + 1
            self._draw()
