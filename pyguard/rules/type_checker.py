"""
类型检查规则模块

检测类型标注相关问题，包括缺少返回类型标注、使用Any类型、
类型不一致赋值、缺少参数类型标注、Optional类型未正确处理等。
"""

import ast
from typing import Any, Dict, List

from ..models import BaseRule, Issue


class TypeChecker(BaseRule):
    """类型检查规则集合"""

    rule_id = "TYPE"
    description = "类型检查规则"
    severity = "info"
    category = "type"

    def __init__(self, config: Dict[str, Any] = None):
        """初始化类型检查器

        Args:
            config: 配置字典
        """
        self.config = config or {}

    def check(self, tree: ast.AST, file_path: str, lines: List[str]) -> List[Issue]:
        """执行类型检查

        Args:
            tree: AST语法树
            file_path: 文件路径
            lines: 文件行列表

        Returns:
            问题列表
        """
        issues: List[Issue] = []
        issues.extend(self._check_missing_return_type(tree, file_path))
        issues.extend(self._check_any_usage(tree, file_path))
        issues.extend(self._check_missing_param_types(tree, file_path))
        issues.extend(self._check_optional_handling(tree, file_path))
        issues.extend(self._check_type_inconsistency(tree, file_path))
        return issues

    def _check_missing_return_type(
        self, tree: ast.AST, file_path: str
    ) -> List[Issue]:
        """检测未标注返回类型的函数

        Args:
            tree: AST语法树
            file_path: 文件路径

        Returns:
            问题列表
        """
        issues: List[Issue] = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # 跳过魔术方法和私有方法
                if node.name.startswith("__") and node.name.endswith("__"):
                    continue
                if node.returns is None:
                    issues.append(Issue(
                        file_path=file_path,
                        line_no=node.lineno,
                        column=node.col_offset,
                        rule_id="TYPE001",
                        severity="info",
                        message=f"函数 '{node.name}' 缺少返回类型标注",
                        category="type",
                        suggestion=f"def {node.name}(...) -> ReturnType:",
                    ))
        return issues

    def _check_any_usage(self, tree: ast.AST, file_path: str) -> List[Issue]:
        """检测使用Any类型

        Args:
            tree: AST语法树
            file_path: 文件路径

        Returns:
            问题列表
        """
        issues: List[Issue] = []

        def _check_annotation(annotation: ast.AST) -> None:
            """递归检查类型标注中是否使用了Any"""
            if isinstance(annotation, ast.Name) and annotation.id == "Any":
                issues.append(Issue(
                    file_path=file_path,
                    line_no=annotation.lineno,
                    column=annotation.col_offset,
                    rule_id="TYPE002",
                    severity="warning",
                    message="使用了 Any 类型，建议使用更具体的类型",
                    category="type",
                    suggestion="使用具体的类型替代 Any",
                ))
            elif isinstance(annotation, ast.Subscript):
                _check_annotation(annotation.value)

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # 检查参数类型标注
                for default in node.args.args:
                    if default.annotation:
                        _check_annotation(default.annotation)
                # 检查返回类型标注
                if node.returns:
                    _check_annotation(node.returns)
            elif isinstance(node, ast.AnnAssign):
                if node.annotation:
                    _check_annotation(node.annotation)
        return issues

    def _check_missing_param_types(
        self, tree: ast.AST, file_path: str
    ) -> List[Issue]:
        """检测缺少参数类型标注

        Args:
            tree: AST语法树
            file_path: 文件路径

        Returns:
            问题列表
        """
        issues: List[Issue] = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # 跳过魔术方法
                if node.name.startswith("__") and node.name.endswith("__"):
                    continue
                # 跳过self和cls
                param_start = 0
                if node.args.args and node.args.args[0].arg in ("self", "cls"):
                    param_start = 1
                for arg in node.args.args[param_start:]:
                    if arg.annotation is None:
                        issues.append(Issue(
                            file_path=file_path,
                            line_no=node.lineno,
                            column=arg.col_offset,
                            rule_id="TYPE003",
                            severity="info",
                            message=f"函数 '{node.name}' 的参数 '{arg.arg}' 缺少类型标注",
                            category="type",
                            suggestion=f"def {node.name}({arg.arg}: Type, ...):",
                        ))
        return issues

    def _check_optional_handling(
        self, tree: ast.AST, file_path: str
    ) -> List[Issue]:
        """检测Optional类型未正确处理

        检查Optional类型的变量在使用前是否进行了None检查。

        Args:
            tree: AST语法树
            file_path: 文件路径

        Returns:
            问题列表
        """
        issues: List[Issue] = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # 查找Optional类型的参数
                for arg in node.args.args:
                    if arg.annotation is None:
                        continue
                    ann_str = ast.dump(arg.annotation)
                    if "Optional" in ann_str or "Union" in ann_str:
                        # 检查函数体中是否有对None的检查
                        has_none_check = False
                        for child in ast.walk(node):
                            if isinstance(child, ast.Compare):
                                for comparator in child.comparators:
                                    if isinstance(comparator, ast.Constant) and comparator.value is None:
                                        has_none_check = True
                                    elif isinstance(comparator, ast.NameConstant) and comparator.value is None:
                                        has_none_check = True
                            elif isinstance(child, ast.IfExp):
                                test_str = ast.dump(child.test)
                                if "None" in test_str:
                                    has_none_check = True
                        if not has_none_check:
                            issues.append(Issue(
                                file_path=file_path,
                                line_no=node.lineno,
                                column=arg.col_offset,
                                rule_id="TYPE004",
                                severity="warning",
                                message=f"Optional参数 '{arg.arg}' 使用前未进行None检查",
                                category="type",
                                suggestion=f"在使用 '{arg.arg}' 前添加 if {arg.arg} is not None 检查",
                            ))
        return issues

    def _check_type_inconsistency(
        self, tree: ast.AST, file_path: str
    ) -> List[Issue]:
        """检测类型不一致的赋值

        同一变量在不同位置被赋予不同类型的值。

        Args:
            tree: AST语法树
            file_path: 文件路径

        Returns:
            问题列表
        """
        issues: List[Issue] = []
        var_types: Dict[str, List[tuple]] = {}

        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        var_name = target.id
                        # 推断赋值类型
                        value_type = self._infer_type(node.value)
                        if value_type:
                            if var_name not in var_types:
                                var_types[var_name] = []
                            var_types[var_name].append(
                                (value_type, node.lineno)
                            )

        # 检查同一变量是否有不同类型
        for var_name, type_list in var_types.items():
            unique_types = set(t[0] for t in type_list)
            if len(unique_types) > 1:
                issues.append(Issue(
                    file_path=file_path,
                    line_no=type_list[0][1],
                    column=0,
                    rule_id="TYPE005",
                    severity="warning",
                    message=f"变量 '{var_name}' 被赋予了不同类型的值: {', '.join(unique_types)}",
                    category="type",
                    suggestion="确保变量类型一致，或使用 Union 类型标注",
                ))
        return issues

    @staticmethod
    def _infer_type(node: ast.AST) -> str:
        """推断表达式的类型

        Args:
            node: AST节点

        Returns:
            推断的类型字符串
        """
        if isinstance(node, ast.Constant):
            val = node.value
            if isinstance(val, int):
                return "int"
            elif isinstance(val, float):
                return "float"
            elif isinstance(val, str):
                return "str"
            elif isinstance(val, bool):
                return "bool"
            elif val is None:
                return "None"
        elif isinstance(node, ast.List):
            return "list"
        elif isinstance(node, ast.Dict):
            return "dict"
        elif isinstance(node, ast.Tuple):
            return "tuple"
        elif isinstance(node, ast.Set):
            return "set"
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                return node.func.id
        return ""
