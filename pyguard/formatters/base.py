"""
格式化器基类和工厂函数

定义输出格式化器的统一接口，提供工厂函数获取对应格式化器实例。
"""

import json
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..scanner import ScanResult

from ..utils import (
    bold, red, green, yellow, blue, cyan, magenta,
    colorize, severity_to_color, severity_to_symbol, get_line_content,
    Colors,
)


class BaseFormatter(ABC):
    """输出格式化器基类"""

    @abstractmethod
    def format(self, result: "ScanResult") -> str:
        """格式化扫描结果

        Args:
            result: 扫描结果

        Returns:
            格式化后的字符串
        """
        raise NotImplementedError


class TextFormatter(BaseFormatter):
    """彩色终端文本格式化器"""

    def format(self, result: "ScanResult") -> str:
        """格式化为彩色终端输出

        Args:
            result: 扫描结果

        Returns:
            格式化后的文本
        """
        lines: list = []

        # 标题
        lines.append("")
        lines.append(bold("=" * 60))
        lines.append(bold("  PyGuard-CLI 代码质量巡检报告"))
        lines.append(bold("=" * 60))
        lines.append("")

        # 摘要
        lines.append(self._format_summary(result))
        lines.append("")

        # 问题列表
        if result.issues:
            lines.append(bold("-" * 60))
            lines.append(bold(f"  发现 {len(result.issues)} 个问题"))
            lines.append(bold("-" * 60))

            current_file = ""
            for issue in result.issues:
                if issue.file_path != current_file:
                    current_file = issue.file_path
                    lines.append("")
                    lines.append(bold(f"  {cyan(current_file)}"))

                sym = severity_to_symbol(issue.severity)
                color = severity_to_color(issue.severity)
                lines.append(
                    f"    {colorize(f'[{sym}]', color)} "
                    f"{bold(issue.rule_id)} "
                    f"第{issue.line_no}列{issue.column} "
                    f"- {issue.message}"
                )
                if issue.suggestion:
                    lines.append(f"      {magenta('建议:')} {issue.suggestion}")
        else:
            lines.append(green("  未发现问题，代码质量良好!"))

        lines.append("")
        lines.append(bold("=" * 60))
        return "\n".join(lines)

    def _format_summary(self, result: "ScanResult") -> str:
        """格式化摘要信息

        Args:
            result: 扫描结果

        Returns:
            摘要文本
        """
        lines: list = []
        lines.append(bold("  摘要:"))
        lines.append(f"    扫描文件数:   {result.files_scanned}")
        lines.append(f"    问题文件数:   {result.files_with_issues}")
        lines.append(f"    代码总行数:   {result.total_lines}")
        lines.append(f"    扫描耗时:     {result.scan_time:.3f}s")
        lines.append("")
        lines.append(f"    {red('错误:')} {result.error_count}  "
                     f"{yellow('警告:')} {result.warning_count}  "
                     f"{cyan('信息:')} {result.info_count}  "
                     f"{bold('总计:')} {len(result.issues)}")
        return "\n".join(lines)


def get_formatter(fmt: str) -> BaseFormatter:
    """获取指定格式的格式化器实例

    Args:
        fmt: 格式名称 (text/json/html/markdown)

    Returns:
        对应的格式化器实例
    """
    from .json_fmt import JsonFormatter
    from .html_fmt import HtmlFormatter
    from .markdown_fmt import MarkdownFormatter

    formatters = {
        "text": TextFormatter,
        "json": JsonFormatter,
        "html": HtmlFormatter,
        "markdown": MarkdownFormatter,
    }
    formatter_cls = formatters.get(fmt, TextFormatter)
    return formatter_cls()
