"""
代码风格检查规则模块

检测代码风格相关问题，包括行长度、docstring缺失、命名规范、
尾随空格/空行、导入顺序等。
"""

import ast
import re
from typing import Any, Dict, List

from ..models import BaseRule, Issue


class StyleChecker(BaseRule):
    """代码风格检查规则集合"""

    rule_id = "STYLE"
    description = "代码风格检查规则"
    severity = "info"
    category = "style"

    def __init__(self, config: Dict[str, Any] = None):
        """初始化代码风格检查器

        Args:
            config: 配置字典
        """
        self.config = config or {}
        self.max_line_length: int = self.config.get("max_line_length", 120)

    def check(self, tree: ast.AST, file_path: str, lines: List[str]) -> List[Issue]:
        """执行代码风格检查

        Args:
            tree: AST语法树
            file_path: 文件路径
            lines: 文件行列表

        Returns:
            问题列表
        """
        issues: List[Issue] = []
        issues.extend(self._check_line_length(file_path, lines))
        issues.extend(self._check_missing_docstring(tree, file_path))
        issues.extend(self._check_naming_convention(tree, file_path))
        issues.extend(self._check_trailing_whitespace(file_path, lines))
        issues.extend(self._check_import_order(tree, file_path))
        return issues

    def _check_line_length(
        self, file_path: str, lines: List[str]
    ) -> List[Issue]:
        """检测行长度超过限制

        Args:
            file_path: 文件路径
            lines: 文件行列表

        Returns:
            问题列表
        """
        issues: List[Issue] = []
        for i, line in enumerate(lines, 1):
            # 跳过注释中的长URL
            stripped = line.strip()
            if stripped.startswith("#") and "http" in stripped:
                continue
            if len(line) > self.max_line_length:
                issues.append(Issue(
                    file_path=file_path,
                    line_no=i,
                    column=self.max_line_length,
                    rule_id="STYLE001",
                    severity="warning",
                    message=f"行长度 {len(line)} 超过限制 {self.max_line_length}",
                    category="style",
                    suggestion="将长行拆分为多行",
                ))
        return issues

    def _check_missing_docstring(
        self, tree: ast.AST, file_path: str
    ) -> List[Issue]:
        """检测函数/类缺少docstring

        Args:
            tree: AST语法树
            file_path: 文件路径

        Returns:
            问题列表
        """
        issues: List[Issue] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                docstring = ast.get_docstring(node)
                if not docstring:
                    issues.append(Issue(
                        file_path=file_path,
                        line_no=node.lineno,
                        column=node.col_offset,
                        rule_id="STYLE002",
                        severity="info",
                        message=f"类 '{node.name}' 缺少docstring",
                        category="style",
                        suggestion='添加类文档字符串，例如: """类描述"""',
                    ))
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # 跳过私有方法和魔术方法
                if node.name.startswith("_"):
                    continue
                docstring = ast.get_docstring(node)
                if not docstring:
                    prefix = "异步函数" if isinstance(node, ast.AsyncFunctionDef) else "函数"
                    issues.append(Issue(
                        file_path=file_path,
                        line_no=node.lineno,
                        column=node.col_offset,
                        rule_id="STYLE003",
                        severity="info",
                        message=f"{prefix} '{node.name}' 缺少docstring",
                        category="style",
                        suggestion='添加函数文档字符串',
                    ))
        return issues

    def _check_naming_convention(
        self, tree: ast.AST, file_path: str
    ) -> List[Issue]:
        """检测命名不规范

        检查函数名、变量名是否符合snake_case规范，
        类名是否符合PascalCase规范。

        Args:
            tree: AST语法树
            file_path: 文件路径

        Returns:
            问题列表
        """
        issues: List[Issue] = []
        snake_pattern = re.compile(r"^[a-z_][a-z0-9_]*$")
        pascal_pattern = re.compile(r"^[A-Z][a-zA-Z0-9]*$")
        upper_pattern = re.compile(r"^[A-Z_][A-Z0-9_]*$")

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if not pascal_pattern.match(node.name):
                    issues.append(Issue(
                        file_path=file_path,
                        line_no=node.lineno,
                        column=node.col_offset,
                        rule_id="STYLE004",
                        severity="warning",
                        message=f"类名 '{node.name}' 不符合PascalCase命名规范",
                        category="style",
                        suggestion="类名应使用PascalCase (如: MyClass)",
                    ))
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # 跳过魔术方法
                if node.name.startswith("__") and node.name.endswith("__"):
                    continue
                # 常量风格函数（全大写）也允许
                if upper_pattern.match(node.name):
                    continue
                if not snake_pattern.match(node.name):
                    issues.append(Issue(
                        file_path=file_path,
                        line_no=node.lineno,
                        column=node.col_offset,
                        rule_id="STYLE005",
                        severity="warning",
                        message=f"函数名 '{node.name}' 不符合snake_case命名规范",
                        category="style",
                        suggestion="函数名应使用snake_case (如: my_function)",
                    ))
        return issues

    def _check_trailing_whitespace(
        self, file_path: str, lines: List[str]
    ) -> List[Issue]:
        """检测尾随空格和多余空行

        Args:
            file_path: 文件路径
            lines: 文件行列表

        Returns:
            问题列表
        """
        issues: List[Issue] = []
        consecutive_blank = 0

        for i, line in enumerate(lines, 1):
            # 检测尾随空格
            if line != line.rstrip():
                issues.append(Issue(
                    file_path=file_path,
                    line_no=i,
                    column=len(line.rstrip()) + 1,
                    rule_id="STYLE006",
                    severity="info",
                    message="行末有多余空格",
                    category="style",
                    suggestion="删除行末空格",
                ))

            # 检测连续空行（超过2个）
            if line.strip() == "":
                consecutive_blank += 1
                if consecutive_blank > 2:
                    issues.append(Issue(
                        file_path=file_path,
                        line_no=i,
                        column=0,
                        rule_id="STYLE007",
                        severity="info",
                        message="连续空行超过2行",
                        category="style",
                        suggestion="最多保留2个连续空行",
                    ))
            else:
                consecutive_blank = 0

        return issues

    def _check_import_order(
        self, tree: ast.AST, file_path: str
    ) -> List[Issue]:
        """检测导入顺序不规范

        标准库导入应在第三方库之前，本地导入应在最后。
        各分组之间应有空行分隔。

        Args:
            tree: AST语法树
            file_path: 文件路径

        Returns:
            问题列表
        """
        issues: List[Issue] = []
        imports: List[tuple] = []

        stdlib_modules = {
            "os", "sys", "re", "json", "ast", "io", "math", "time",
            "datetime", "collections", "itertools", "functools", "typing",
            "pathlib", "subprocess", "threading", "logging", "argparse",
            "hashlib", "base64", "copy", "operator", "abc", "dataclasses",
            "enum", "contextlib", "unittest", "traceback", "warnings",
            "socket", "http", "urllib", "email", "html", "xml", "csv",
            "sqlite3", "tempfile", "shutil", "glob", "fnmatch", "random",
            "string", "textwrap", "struct", "array", "queue", "select",
            "signal", "mmap", "ctypes", "concurrent", "multiprocessing",
        }

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    top_module = alias.name.split(".")[0]
                    group = "stdlib" if top_module in stdlib_modules else "third_party"
                    imports.append((node.lineno, group, alias.name))
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    top_module = node.module.split(".")[0]
                    group = "stdlib" if top_module in stdlib_modules else "third_party"
                else:
                    group = "relative"
                imports.append((node.lineno, group, node.module or "."))

        # 检查导入顺序：stdlib -> third_party -> relative
        prev_group_order = {"stdlib": 0, "third_party": 1, "relative": 2}
        prev_order = -1
        for line_no, group, name in imports:
            current_order = prev_group_order.get(group, 1)
            if current_order < prev_order:
                issues.append(Issue(
                    file_path=file_path,
                    line_no=line_no,
                    column=0,
                    rule_id="STYLE008",
                    severity="info",
                    message=f"导入 '{name}' 顺序不规范，标准库导入应在第三方库之前",
                    category="style",
                    suggestion="按 标准库 -> 第三方库 -> 本地模块 的顺序组织导入",
                ))
            prev_order = max(prev_order, current_order)

        return issues
