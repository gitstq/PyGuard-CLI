"""
PyGuard-CLI 命令行入口

使用argparse实现CLI接口，支持scan和check子命令。
"""

import argparse
import sys
from typing import List, Optional

from . import __version__
from .scanner import Scanner
from .utils import load_config, red, green, yellow, bold, cyan
from .formatters import get_formatter
from .tui.dashboard import TUIChecker


def build_parser() -> argparse.ArgumentParser:
    """构建CLI参数解析器

    Returns:
        配置好的ArgumentParser实例
    """
    parser = argparse.ArgumentParser(
        prog="pyguard",
        description="PyGuard-CLI - 轻量级Python代码质量智能巡检引擎",
        epilog="示例: pyguard scan ./src --format json --severity error",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # scan 子命令
    scan_parser = subparsers.add_parser("scan", help="扫描指定路径下的所有Python文件")
    scan_parser.add_argument("path", help="要扫描的目录或文件路径")
    scan_parser.add_argument(
        "--format", "-f",
        choices=["text", "json", "html", "markdown"],
        default="text",
        help="输出格式 (默认: text)",
    )
    scan_parser.add_argument(
        "--severity", "-s",
        choices=["error", "warning", "info", "all"],
        default="all",
        help="严重级别过滤 (默认: all)",
    )
    scan_parser.add_argument(
        "--ignore", "-i",
        nargs="*",
        default=[],
        help="忽略指定的规则ID",
    )
    scan_parser.add_argument(
        "--config", "-c",
        default=None,
        help="配置文件路径",
    )
    scan_parser.add_argument(
        "--parallel", "-p",
        action="store_true",
        help="启用并行扫描",
    )
    scan_parser.add_argument(
        "--tui",
        action="store_true",
        help="启动TUI仪表盘模式",
    )

    # check 子命令
    check_parser = subparsers.add_parser("check", help="检查单个Python文件")
    check_parser.add_argument("file", help="要检查的Python文件路径")
    check_parser.add_argument(
        "--format", "-f",
        choices=["text", "json", "html", "markdown"],
        default="text",
        help="输出格式 (默认: text)",
    )
    check_parser.add_argument(
        "--severity", "-s",
        choices=["error", "warning", "info", "all"],
        default="all",
        help="严重级别过滤 (默认: all)",
    )
    check_parser.add_argument(
        "--ignore", "-i",
        nargs="*",
        default=[],
        help="忽略指定的规则ID",
    )
    check_parser.add_argument(
        "--config", "-c",
        default=None,
        help="配置文件路径",
    )
    check_parser.add_argument(
        "--tui",
        action="store_true",
        help="启动TUI仪表盘模式",
    )

    return parser


def filter_issues(issues: list, severity: str) -> list:
    """根据严重级别过滤问题

    Args:
        issues: 问题列表
        severity: 严重级别过滤条件

    Returns:
        过滤后的问题列表
    """
    if severity == "all":
        return issues
    severity_order = {"error": 0, "warning": 1, "info": 2}
    threshold = severity_order.get(severity, 0)
    return [
        i for i in issues
        if severity_order.get(i.severity, 2) <= threshold
    ]


def main(argv: Optional[List[str]] = None) -> int:
    """CLI主入口函数

    Args:
        argv: 命令行参数列表，为None时使用sys.argv

    Returns:
        退出码（0=无问题, 1=有问题, 2=错误）
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 2

    # 加载配置
    config = load_config(args.config)

    # 合并忽略规则
    ignore_rules = list(config.get("ignore_rules", []))
    ignore_rules.extend(args.ignore)
    config["ignore_rules"] = list(set(ignore_rules))

    # 初始化扫描器
    scanner = Scanner(config)

    # 执行扫描
    if args.command == "scan":
        result = scanner.scan_path(args.path, parallel=args.parallel)
    elif args.command == "check":
        result = scanner.check_single_file(args.file)
    else:
        parser.print_help()
        return 2

    # 检查是否有扫描错误
    if result.errors:
        for err in result.errors:
            print(red(f"错误: {err}"), file=sys.stderr)
        if not result.issues:
            return 2

    # 过滤问题
    filtered_issues = filter_issues(result.issues, args.severity)
    result.issues = filtered_issues

    # TUI模式
    if hasattr(args, "tui") and args.tui:
        tui = TUIChecker(result)
        tui.run()
        return 1 if result.error_count > 0 else 0

    # 格式化输出
    formatter = get_formatter(args.format)
    output = formatter.format(result)

    if args.format == "json":
        print(output)
    elif args.format == "html":
        print(output)
    elif args.format == "markdown":
        print(output)
    else:
        print(output)

    # 返回退出码
    if result.error_count > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
