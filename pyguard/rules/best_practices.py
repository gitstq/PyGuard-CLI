"""
Python最佳实践检查规则模块

检测不符合Python最佳实践的代码，包括过于宽泛的异常处理、
可变默认参数、未使用的导入/变量、缺少__init__方法等。
"""

import ast
from typing import Any, Dict, List, Set

from ..models import BaseRule, Issue


class BestPracticesChecker(BaseRule):
    """Python最佳实践检查规则集合"""

    rule_id = "BP"
    description = "Python最佳实践检查规则"
    severity = "warning"
    category = "best_practice"

    def __init__(self, config: Dict[str, Any] = None):
        """初始化最佳实践检查器

        Args:
            config: 配置字典
        """
        self.config = config or {}

    def check(self, tree: ast.AST, file_path: str, lines: List[str]) -> List[Issue]:
        """执行最佳实践检查

        Args:
            tree: AST语法树
            file_path: 文件路径
            lines: 文件行列表

        Returns:
            问题列表
        """
        issues: List[Issue] = []
        issues.extend(self._check_bare_except(tree, file_path))
        issues.extend(self._check_mutable_default_args(tree, file_path))
        issues.extend(self._check_unused_imports(tree, file_path))
        issues.extend(self._check_unused_variables(tree, file_path))
        issues.extend(self._check_missing_init(tree, file_path))
        return issues

    def _check_bare_except(
        self, tree: ast.AST, file_path: str
    ) -> List[Issue]:
        """检测过于宽泛的异常处理（bare except）

        Args:
            tree: AST语法树
            file_path: 文件路径

        Returns:
            问题列表
        """
        issues: List[Issue] = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler):
                if node.type is None:
                    issues.append(Issue(
                        file_path=file_path,
                        line_no=node.lineno,
                        column=node.col_offset,
                        rule_id="BP001",
                        severity="warning",
                        message="使用了裸 except，会捕获所有异常包括 KeyboardInterrupt",
                        category="best_practice",
                        suggestion="使用 except Exception: 替代裸 except",
                    ))
                elif isinstance(node.type, ast.Name) and node.type.id == "Exception":
                    issues.append(Issue(
                        file_path=file_path,
                        line_no=node.lineno,
                        column=node.col_offset,
                        rule_id="BP001",
                        severity="info",
                        message="捕获了过于宽泛的 Exception，建议捕获更具体的异常类型",
                        category="best_practice",
                        suggestion="捕获具体的异常类型如 ValueError, TypeError 等",
                    ))
        return issues

    def _check_mutable_default_args(
        self, tree: ast.AST, file_path: str
    ) -> List[Issue]:
        """检测使用可变对象作为默认参数

        Args:
            tree: AST语法树
            file_path: 文件路径

        Returns:
            问题列表
        """
        issues: List[Issue] = []
        mutable_types = (ast.List, ast.Dict, ast.Set)

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for default in node.args.defaults + node.args.kw_defaults:
                    if default is None:
                        continue
                    if isinstance(default, mutable_types):
                        issues.append(Issue(
                            file_path=file_path,
                            line_no=node.lineno,
                            column=default.col_offset,
                            rule_id="BP002",
                            severity="error",
                            message=f"函数 '{node.name}' 使用了可变默认参数",
                            category="best_practice",
                            suggestion="使用 None 作为默认值，在函数体内创建可变对象",
                        ))
        return issues

    def _check_unused_imports(
        self, tree: ast.AST, file_path: str
    ) -> List[Issue]:
        """检测未使用的导入

        Args:
            tree: AST语法树
            file_path: 文件路径

        Returns:
            问题列表
        """
        issues: List[Issue] = []

        # 收集所有导入
        imports: Dict[str, tuple] = {}
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    name = alias.asname if alias.asname else alias.name.split(".")[0]
                    imports[name] = (node.lineno, alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.names:
                    for alias in node.names:
                        if alias.name == "*":
                            continue
                        name = alias.asname if alias.asname else alias.name
                        imports[name] = (node.lineno, alias.name)

        if not imports:
            return issues

        # 收集所有使用的名称
        used_names: Set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                used_names.add(node.id)
            elif isinstance(node, ast.Attribute):
                if isinstance(node.value, ast.Name):
                    used_names.add(node.value.id)

        # 检查未使用的导入
        for name, (line_no, full_name) in imports.items():
            if name not in used_names:
                issues.append(Issue(
                    file_path=file_path,
                    line_no=line_no,
                    column=0,
                    rule_id="BP003",
                    severity="info",
                    message=f"导入 '{full_name}' 未被使用",
                    category="best_practice",
                    suggestion=f"删除未使用的导入: {full_name}",
                ))
        return issues

    def _check_unused_variables(
        self, tree: ast.AST, file_path: str
    ) -> List[Issue]:
        """检测未使用的变量

        Args:
            tree: AST语法树
            file_path: 文件路径

        Returns:
            问题列表
        """
        issues: List[Issue] = []

        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue

            # 收集函数内赋值的变量
            assigned_vars: Dict[str, int] = {}
            # 收集函数内使用的变量
            used_vars: Set[str] = set()

            for child in ast.walk(node):
                if isinstance(child, ast.Assign):
                    for target in child.targets:
                        if isinstance(target, ast.Name):
                            assigned_vars[target.id] = child.lineno
                        elif isinstance(target, ast.Tuple):
                            for elt in target.elts:
                                if isinstance(elt, ast.Name):
                                    assigned_vars[elt.id] = child.lineno
                elif isinstance(child, ast.Name) and isinstance(child.ctx, ast.Load):
                    used_vars.add(child.id)

            # 跳过以下划线开头的变量
            for var_name, line_no in assigned_vars.items():
                if var_name.startswith("_"):
                    continue
                if var_name not in used_vars:
                    issues.append(Issue(
                        file_path=file_path,
                        line_no=line_no,
                        column=0,
                        rule_id="BP004",
                        severity="info",
                        message=f"变量 '{var_name}' 已赋值但未使用",
                        category="best_practice",
                        suggestion=f"删除未使用的变量或以 '_' 前缀标记",
                    ))
        return issues

    def _check_missing_init(
        self, tree: ast.AST, file_path: str
    ) -> List[Issue]:
        """检测类缺少 __init__ 方法定义

        对于有实例方法的类，应定义 __init__ 方法。

        Args:
            tree: AST语法树
            file_path: 文件路径

        Returns:
            问题列表
        """
        issues: List[Issue] = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # 跳过异常基类和简单数据类
                if node.name in ("Exception", "BaseException", "object"):
                    continue

                has_init = False
                has_methods = False
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        if item.name == "__init__":
                            has_init = True
                            break
                        if not item.name.startswith("_"):
                            has_methods = True

                if has_methods and not has_init:
                    issues.append(Issue(
                        file_path=file_path,
                        line_no=node.lineno,
                        column=node.col_offset,
                        rule_id="BP005",
                        severity="info",
                        message=f"类 '{node.name}' 缺少 __init__ 方法定义",
                        category="best_practice",
                        suggestion="为类添加 __init__ 方法以初始化实例属性",
                    ))
        return issues
