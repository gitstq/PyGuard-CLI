"""
PyGuard-CLI 工具函数模块

提供通用的辅助函数，包括ANSI颜色输出、文件查找、配置加载等功能。
"""

import os
import re
import json
import sys
from typing import Any, Dict, List, Optional, Tuple


# ANSI 颜色代码
class Colors:
    """ANSI 终端颜色代码常量"""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"


def colorize(text: str, color: str) -> str:
    """为文本添加ANSI颜色

    Args:
        text: 要着色的文本
        color: ANSI颜色代码

    Returns:
        着色后的文本
    """
    if not sys.stdout.isatty():
        return text
    return f"{color}{text}{Colors.RESET}"


def bold(text: str) -> str:
    """加粗文本"""
    return colorize(text, Colors.BOLD)


def red(text: str) -> str:
    """红色文本"""
    return colorize(text, Colors.RED)


def green(text: str) -> str:
    """绿色文本"""
    return colorize(text, Colors.GREEN)


def yellow(text: str) -> str:
    """黄色文本"""
    return colorize(text, Colors.YELLOW)


def blue(text: str) -> str:
    """蓝色文本"""
    return colorize(text, Colors.BLUE)


def cyan(text: str) -> str:
    """青色文本"""
    return colorize(text, Colors.CYAN)


def magenta(text: str) -> str:
    """品红色文本"""
    return colorize(text, Colors.MAGENTA)


def find_python_files(path: str) -> List[str]:
    """递归查找指定路径下的所有Python文件

    Args:
        path: 要搜索的目录或文件路径

    Returns:
        找到的Python文件绝对路径列表
    """
    if os.path.isfile(path):
        if path.endswith(".py"):
            return [os.path.abspath(path)]
        return []

    py_files: List[str] = []
    for root, _dirs, files in os.walk(path):
        for f in files:
            if f.endswith(".py"):
                py_files.append(os.path.abspath(os.path.join(root, f)))
    return sorted(py_files)


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """加载配置文件

    支持JSON格式的配置文件，如果未指定则查找默认配置文件。

    Args:
        config_path: 配置文件路径，为None时自动查找

    Returns:
        配置字典
    """
    default_config: Dict[str, Any] = {
        "max_line_length": 120,
        "max_complexity": 10,
        "max_function_length": 50,
        "max_nesting_depth": 4,
        "max_parameters": 7,
        "max_class_length": 500,
        "severity": "all",
        "ignore_rules": [],
    }

    if config_path is None:
        # 自动查找配置文件
        for name in ["pyguard.json", ".pyguard.json"]:
            if os.path.exists(name):
                config_path = name
                break

    if config_path and os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                user_config = json.load(f)
            default_config.update(user_config)
        except (json.JSONDecodeError, IOError) as e:
            print(yellow(f"警告: 无法加载配置文件 {config_path}: {e}"))

    return default_config


def get_line_content(file_path: str, line_no: int) -> str:
    """获取文件指定行的内容

    Args:
        file_path: 文件路径
        line_no: 行号（从1开始）

    Returns:
        该行的文本内容
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            if 1 <= line_no <= len(lines):
                return lines[line_no - 1].rstrip("\n\r")
    except IOError:
        pass
    return ""


def format_file_size(size_bytes: int) -> str:
    """格式化文件大小

    Args:
        size_bytes: 文件大小（字节）

    Returns:
        人类可读的文件大小字符串
    """
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def count_lines(file_path: str) -> int:
    """统计文件行数

    Args:
        file_path: 文件路径

    Returns:
        文件总行数
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return sum(1 for _ in f)
    except IOError:
        return 0


def severity_to_color(severity: str) -> str:
    """将严重级别转换为对应的颜色

    Args:
        severity: 严重级别（error/warning/info）

    Returns:
        ANSI颜色代码
    """
    mapping = {
        "error": Colors.RED,
        "warning": Colors.YELLOW,
        "info": Colors.CYAN,
    }
    return mapping.get(severity.lower(), Colors.WHITE)


def severity_to_symbol(severity: str) -> str:
    """将严重级别转换为对应的符号

    Args:
        severity: 严重级别（error/warning/info）

    Returns:
        对应的Unicode符号
    """
    mapping = {
        "error": "x",
        "warning": "!",
        "info": "i",
    }
    return mapping.get(severity.lower(), "?")
