"""
代码复杂度分析规则模块

分析代码复杂度，包括圈复杂度、函数长度、嵌套层级、
参数数量、类大小等。
"""

import ast
from typing import Any, Dict, List, Optional

from ..models import BaseRule, Issue


class ComplexityChecker(BaseRule):
    """代码复杂度分析规则集合"""

    rule_id = "CPLX"
    description = "代码复杂度分析规则"
    severity = "warning"
    category = "complexity"

    def __init__(self, config: Dict[str, Any] = None):
        """初始化复杂度检查器

        Args:
            config: 配置字典
        """
        self.config = config or {}
        self.max_complexity: int = self.config.get("max_complexity", 10)
        self.max_function_length: int = self.config.get("max_function_length", 50)
        self.max_nesting_depth: int = self.config.get("max_nesting_depth", 4)
        self.max_parameters: int = self.config.get("max_parameters", 7)
        self.max_class_length: int = self.config.get("max_class_length", 500)

    def check(self, tree: ast.AST, file_path: str, lines: List[str]) -> List[Issue]:
        """执行复杂度分析

        Args:
            tree: AST语法树
            file_path: 文件路径
            lines: 文件行列表

        Returns:
            问题列表
        """
        issues: List[Issue] = []
        issues.extend(self._check_cyclomatic_complexity(tree, file_path))
        issues.extend(self._check_function_length(tree, file_path, lines))
        issues.extend(self._check_nesting_depth(tree, file_path))
        issues.extend(self._check_parameter_count(tree, file_path))
        issues.extend(self._check_class_size(tree, file_path, lines))
        return issues

    def _check_cyclomatic_complexity(
        self, tree: ast.AST, file_path: str
    ) -> List[Issue]:
        """检测圈复杂度过高的函数

        圈复杂度 = 1 + 分支数（if/for/while/and/or/except等）

        Args:
            tree: AST语法树
            file_path: 文件路径

        Returns:
            问题列表
        """
        issues: List[Issue] = []

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                complexity = self._calculate_complexity(node)
                if complexity > self.max_complexity:
                    issues.append(Issue(
                        file_path=file_path,
                        line_no=node.lineno,
                        column=node.col_offset,
                        rule_id="CPLX001",
                        severity="warning",
                        message=f"函数 '{node.name}' 圈复杂度为 {complexity}，超过限制 {self.max_complexity}",
                        category="complexity",
                        suggestion="将复杂函数拆分为多个小函数以降低圈复杂度",
                    ))
        return issues

    def _calculate_complexity(self, node: ast.AST) -> int:
        """计算AST节点的圈复杂度

        Args:
            node: AST节点

        Returns:
            圈复杂度值
        """
        complexity = 1
        for child in ast.walk(node):
            if child is node:
                continue
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
            elif isinstance(child, (ast.And, ast.Or)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
            elif isinstance(child, ast.comprehension):
                complexity += 1
                if child.ifs:
                    complexity += len(child.ifs)
        return complexity

    def _check_function_length(
        self, tree: ast.AST, file_path: str, lines: List[str]
    ) -> List[Issue]:
        """检测函数过长

        Args:
            tree: AST语法树
            file_path: 文件路径
            lines: 文件行列表

        Returns:
            问题列表
        """
        issues: List[Issue] = []

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                func_length = node.end_lineno - node.lineno + 1 if node.end_lineno else 0
                if func_length > self.max_function_length:
                    issues.append(Issue(
                        file_path=file_path,
                        line_no=node.lineno,
                        column=node.col_offset,
                        rule_id="CPLX002",
                        severity="warning",
                        message=f"函数 '{node.name}' 有 {func_length} 行，超过限制 {self.max_function_length} 行",
                        category="complexity",
                        suggestion="将长函数拆分为多个小函数",
                    ))
        return issues

    def _check_nesting_depth(
        self, tree: ast.AST, file_path: str
    ) -> List[Issue]:
        """检测嵌套层级过深

        Args:
            tree: AST语法树
            file_path: 文件路径

        Returns:
            问题列表
        """
        issues: List[Issue] = []

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                max_depth = self._calculate_nesting_depth(node)
                if max_depth > self.max_nesting_depth:
                    issues.append(Issue(
                        file_path=file_path,
                        line_no=node.lineno,
                        column=node.col_offset,
                        rule_id="CPLX003",
                        severity="warning",
                        message=f"函数 '{node.name}' 最大嵌套深度为 {max_depth}，超过限制 {self.max_nesting_depth}",
                        category="complexity",
                        suggestion="使用提前返回(early return)或提取子函数来减少嵌套",
                    ))
        return issues

    def _calculate_nesting_depth(self, node: ast.AST, depth: int = 0) -> int:
        """计算AST节点的最大嵌套深度

        Args:
            node: AST节点
            depth: 当前深度

        Returns:
            最大嵌套深度
        """
        max_depth = depth
        nesting_nodes = (
            ast.If, ast.For, ast.While, ast.With, ast.AsyncWith,
            ast.Try, ast.ExceptHandler,
        )
        for child in ast.iter_child_nodes(node):
            if isinstance(child, nesting_nodes):
                child_depth = self._calculate_nesting_depth(child, depth + 1)
                max_depth = max(max_depth, child_depth)
            else:
                child_depth = self._calculate_nesting_depth(child, depth)
                max_depth = max(max_depth, child_depth)
        return max_depth

    def _check_parameter_count(
        self, tree: ast.AST, file_path: str
    ) -> List[Issue]:
        """检测函数参数过多

        Args:
            tree: AST语法树
            file_path: 文件路径

        Returns:
            问题列表
        """
        issues: List[Issue] = []

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # 计算参数数量（不包括self/cls）
                param_count = len(node.args.args)
                param_count += len(node.args.kwonlyargs)
                if node.args.vararg:
                    param_count += 1
                if node.args.kwarg:
                    param_count += 1
                # 减去self/cls
                if node.args.args and node.args.args[0].arg in ("self", "cls"):
                    param_count -= 1

                if param_count > self.max_parameters:
                    issues.append(Issue(
                        file_path=file_path,
                        line_no=node.lineno,
                        column=node.col_offset,
                        rule_id="CPLX004",
                        severity="warning",
                        message=f"函数 '{node.name}' 有 {param_count} 个参数，超过限制 {self.max_parameters}",
                        category="complexity",
                        suggestion="将参数封装为数据类或字典，或使用*args/**kwargs",
                    ))
        return issues

    def _check_class_size(
        self, tree: ast.AST, file_path: str, lines: List[str]
    ) -> List[Issue]:
        """检测类过大

        Args:
            tree: AST语法树
            file_path: 文件路径
            lines: 文件行列表

        Returns:
            问题列表
        """
        issues: List[Issue] = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_length = node.end_lineno - node.lineno + 1 if node.end_lineno else 0
                if class_length > self.max_class_length:
                    issues.append(Issue(
                        file_path=file_path,
                        line_no=node.lineno,
                        column=node.col_offset,
                        rule_id="CPLX005",
                        severity="warning",
                        message=f"类 '{node.name}' 有 {class_length} 行，超过限制 {self.max_class_length} 行",
                        category="complexity",
                        suggestion="将大类拆分为多个小类，使用组合替代继承",
                    ))
        return issues
