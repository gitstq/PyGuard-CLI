"""
性能优化建议规则模块

检测代码中可能存在的性能问题，包括循环中字符串拼接、
不必要的列表推导、全局变量查找、大量字符串连接、
循环中重复函数调用等。
"""

import ast
from typing import Any, Dict, List

from ..models import BaseRule, Issue


class PerformanceChecker(BaseRule):
    """性能优化建议规则集合"""

    rule_id = "PERF"
    description = "性能优化建议规则"
    severity = "info"
    category = "performance"

    def __init__(self, config: Dict[str, Any] = None):
        """初始化性能检查器

        Args:
            config: 配置字典
        """
        self.config = config or {}

    def check(self, tree: ast.AST, file_path: str, lines: List[str]) -> List[Issue]:
        """执行性能检查

        Args:
            tree: AST语法树
            file_path: 文件路径
            lines: 文件行列表

        Returns:
            问题列表
        """
        issues: List[Issue] = []
        issues.extend(self._check_string_concat_in_loop(tree, file_path))
        issues.extend(self._check_unnecessary_list_comp(tree, file_path))
        issues.extend(self._check_global_variable_lookup(tree, file_path))
        issues.extend(self._check_string_plus_concat(tree, file_path))
        issues.extend(self._check_repeated_call_in_loop(tree, file_path))
        return issues

    def _check_string_concat_in_loop(
        self, tree: ast.AST, file_path: str
    ) -> List[Issue]:
        """检测循环中字符串拼接

        在循环中使用 += 拼接字符串性能较差，应使用 ''.join()。

        Args:
            tree: AST语法树
            file_path: 文件路径

        Returns:
            问题列表
        """
        issues: List[Issue] = []

        for node in ast.walk(tree):
            if isinstance(node, (ast.For, ast.While, ast.AsyncFor)):
                for child in ast.walk(node):
                    if isinstance(child, ast.AugAssign):
                        if isinstance(child.op, ast.Add):
                            if isinstance(child.target, ast.Name):
                                # 检查是否是字符串拼接（通过上下文推断）
                                is_str_concat = False
                                if isinstance(child.value, ast.Constant) and isinstance(child.value.value, str):
                                    is_str_concat = True
                                elif isinstance(child.value, ast.Call):
                                    # str(x) 等转换调用也视为字符串拼接
                                    if isinstance(child.value.func, ast.Name) and child.value.func.id == "str":
                                        is_str_concat = True
                                if is_str_concat:
                                    issues.append(Issue(
                                        file_path=file_path,
                                        line_no=child.lineno,
                                        column=child.col_offset,
                                        rule_id="PERF001",
                                        severity="info",
                                        message=f"循环中使用 += 拼接字符串，建议使用 ''.join()",
                                        category="performance",
                                        suggestion="收集字符串到列表中，最后使用 ''.join(list)",
                                    ))
        return issues

    def _check_unnecessary_list_comp(
        self, tree: ast.AST, file_path: str
    ) -> List[Issue]:
        """检测不必要的列表推导（可用生成器表达式）

        当列表推导仅用于 any()/all()/sum() 等函数时，
        可以使用生成器表达式节省内存。

        Args:
            tree: AST语法树
            file_path: 文件路径

        Returns:
            问题列表
        """
        issues: List[Issue] = []
        lazy_functions = {"any", "all", "sum", "max", "min", "enumerate"}

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in lazy_functions:
                    if node.args and isinstance(node.args[0], ast.ListComp):
                        issues.append(Issue(
                            file_path=file_path,
                            line_no=node.lineno,
                            column=node.col_offset,
                            rule_id="PERF002",
                            severity="info",
                            message=f"在 {node.func.id}() 中使用了列表推导，可替换为生成器表达式",
                            category="performance",
                            suggestion=f"将 [...] 替换为 (...) 以使用生成器表达式",
                        ))
        return issues

    def _check_global_variable_lookup(
        self, tree: ast.AST, file_path: str
    ) -> List[Issue]:
        """检测循环中的全局变量查找

        在循环中频繁访问全局变量会降低性能，
        应将全局变量赋值给局部变量。

        Args:
            tree: AST语法树
            file_path: 文件路径

        Returns:
            问题列表
        """
        issues: List[Issue] = []

        # 获取模块级别的全局变量名
        global_names: set = set()
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        global_names.add(target.id)

        if not global_names:
            return issues

        for node in ast.walk(tree):
            if isinstance(node, (ast.For, ast.While, ast.AsyncFor)):
                # 查找循环体中使用的全局变量
                loop_globals = set()
                for child in ast.walk(node):
                    if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Load):
                        if child.id in global_names:
                            loop_globals.add(child.id)

                for var_name in loop_globals:
                    issues.append(Issue(
                        file_path=file_path,
                        line_no=node.lineno,
                        column=node.col_offset,
                        rule_id="PERF003",
                        severity="info",
                        message=f"循环中使用了全局变量 '{var_name}'，建议缓存为局部变量",
                        category="performance",
                        suggestion=f"在循环前添加: {var_name}_local = {var_name}",
                    ))
        return issues

    def _check_string_plus_concat(
        self, tree: ast.AST, file_path: str
    ) -> List[Issue]:
        """检测使用 + 连接大量字符串

        多个字符串使用 + 连接时性能较差。

        Args:
            tree: AST语法树
            file_path: 文件路径

        Returns:
            问题列表
        """
        issues: List[Issue] = []

        for node in ast.walk(tree):
            if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
                # 计算连续的 + 连接数量
                concat_count = self._count_string_concat(node)
                if concat_count >= 3:
                    issues.append(Issue(
                        file_path=file_path,
                        line_no=node.lineno,
                        column=node.col_offset,
                        rule_id="PERF004",
                        severity="info",
                        message=f"使用 + 连接了 {concat_count} 个字符串，建议使用 ''.join() 或 f-string",
                        category="performance",
                        suggestion="使用 ''.join([str1, str2, ...]) 或 f-string",
                    ))
        return issues

    def _count_string_concat(self, node: ast.AST) -> int:
        """计算字符串连接链的长度

        Args:
            node: AST节点

        Returns:
            连接的字符串数量
        """
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            left = self._count_string_concat(node.left)
            right = self._count_string_concat(node.right)
            return left + right
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return 1
        return 1  # 非字符串节点也算一个

    def _check_repeated_call_in_loop(
        self, tree: ast.AST, file_path: str
    ) -> List[Issue]:
        """检测循环中重复调用同一函数

        如果函数的参数不变，应在循环外调用一次。

        Args:
            tree: AST语法树
            file_path: 文件路径

        Returns:
            问题列表
        """
        issues: List[Issue] = []

        for node in ast.walk(tree):
            if isinstance(node, (ast.For, ast.While, ast.AsyncFor)):
                # 收集循环体中的函数调用
                call_signatures: Dict[str, List[int]] = {}
                for child in ast.walk(node):
                    if isinstance(child, ast.Call):
                        sig = ast.dump(child)
                        if isinstance(child.func, ast.Name):
                            name = child.func.id
                            if name not in call_signatures:
                                call_signatures[name] = []
                            call_signatures[name].append(child.lineno)

                # 检查是否有重复调用（同一函数在同一循环中出现多次）
                for func_name, line_nos in call_signatures.items():
                    if len(line_nos) >= 3:
                        issues.append(Issue(
                            file_path=file_path,
                            line_no=node.lineno,
                            column=node.col_offset,
                            rule_id="PERF005",
                            severity="info",
                            message=f"函数 '{func_name}' 在循环中被调用了 {len(line_nos)} 次，考虑缓存结果",
                            category="performance",
                            suggestion=f"如果参数不变，在循环外调用一次并缓存结果",
                        ))
        return issues
