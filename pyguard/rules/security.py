"""
安全漏洞检测规则模块

检测代码中的安全风险，包括eval/exec使用、硬编码密码、
SQL注入风险、不安全的pickle使用、assert做输入验证等。
"""

import ast
import re
from typing import Any, Dict, List

from ..models import BaseRule, Issue


class SecurityChecker(BaseRule):
    """安全漏洞检测规则集合"""

    rule_id = "SEC"
    description = "安全漏洞检测规则"
    severity = "error"
    category = "security"

    def __init__(self, config: Dict[str, Any] = None):
        """初始化安全检查器

        Args:
            config: 配置字典
        """
        self.config = config or {}

    def check(self, tree: ast.AST, file_path: str, lines: List[str]) -> List[Issue]:
        """执行安全检查

        Args:
            tree: AST语法树
            file_path: 文件路径
            lines: 文件行列表

        Returns:
            问题列表
        """
        issues: List[Issue] = []
        issues.extend(self._check_eval_exec(tree, file_path))
        issues.extend(self._check_hardcoded_secrets(file_path, lines))
        issues.extend(self._check_sql_injection(tree, file_path))
        issues.extend(self._check_pickle_usage(tree, file_path))
        issues.extend(self._check_assert_for_input(tree, file_path))
        return issues

    def _check_eval_exec(
        self, tree: ast.AST, file_path: str
    ) -> List[Issue]:
        """检测使用eval()或exec()

        Args:
            tree: AST语法树
            file_path: 文件路径

        Returns:
            问题列表
        """
        issues: List[Issue] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func_name = ""
                if isinstance(node.func, ast.Name):
                    func_name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    func_name = node.func.attr

                if func_name in ("eval", "exec"):
                    issues.append(Issue(
                        file_path=file_path,
                        line_no=node.lineno,
                        column=node.col_offset,
                        rule_id="SEC001",
                        severity="error",
                        message=f"使用了 {func_name}()，存在代码注入风险",
                        category="security",
                        suggestion=f"避免使用 {func_name}()，使用更安全的替代方案如 ast.literal_eval()",
                    ))
        return issues

    def _check_hardcoded_secrets(
        self, file_path: str, lines: List[str]
    ) -> List[Issue]:
        """检测硬编码密码/密钥

        Args:
            file_path: 文件路径
            lines: 文件行列表

        Returns:
            问题列表
        """
        issues: List[Issue] = []
        # 匹配可能包含密码/密钥的变量赋值模式
        secret_patterns = [
            re.compile(
                r'(?i)(password|passwd|pwd|secret|api_key|apikey|token|'
                r'private_key|secret_key|access_key)\s*=\s*["\'][^"\']{3,}["\']'
            ),
            re.compile(
                r'(?i)["\'][A-Za-z0-9+/]{20,}={0,2}["\']'  # 可能的base64密钥
            ),
        ]

        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            # 跳过注释
            if stripped.startswith("#"):
                continue
            # 跳过空字符串或占位符
            if '""' in stripped or "''" in stripped or "None" in stripped:
                continue
            for pattern in secret_patterns:
                if pattern.search(stripped):
                    issues.append(Issue(
                        file_path=file_path,
                        line_no=i,
                        column=0,
                        rule_id="SEC002",
                        severity="error",
                        message="检测到可能的硬编码密码或密钥",
                        category="security",
                        suggestion="使用环境变量或配置文件管理敏感信息",
                    ))
                    break  # 每行只报告一次
        return issues

    def _check_sql_injection(
        self, tree: ast.AST, file_path: str
    ) -> List[Issue]:
        """检测SQL注入风险（字符串拼接SQL）

        Args:
            tree: AST语法树
            file_path: 文件路径

        Returns:
            问题列表
        """
        issues: List[Issue] = []
        sql_keywords = {"SELECT", "INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE"}

        for node in ast.walk(tree):
            if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mod):
                # 检测 % 格式化SQL
                if isinstance(node.left, ast.Constant):
                    left_str = str(node.left.value).upper()
                    if any(kw in left_str for kw in sql_keywords):
                        issues.append(Issue(
                            file_path=file_path,
                            line_no=node.lineno,
                            column=node.col_offset,
                            rule_id="SEC003",
                            severity="error",
                            message="检测到SQL字符串格式化，存在SQL注入风险",
                            category="security",
                            suggestion="使用参数化查询替代字符串格式化",
                        ))

            elif isinstance(node, ast.JoinedStr):
                # 检测f-string SQL
                parts_str = ""
                for value in node.values:
                    if isinstance(value, ast.Constant):
                        parts_str += str(value.value).upper()
                if any(kw in parts_str for kw in sql_keywords):
                    issues.append(Issue(
                        file_path=file_path,
                        line_no=node.lineno,
                        column=node.col_offset,
                        rule_id="SEC003",
                        severity="error",
                        message="检测到f-string拼接SQL，存在SQL注入风险",
                        category="security",
                        suggestion="使用参数化查询替代f-string",
                    ))

            elif isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
                # 检测 + 拼接SQL
                concat_str = self._extract_string_concat(node)
                if concat_str and any(kw in concat_str.upper() for kw in sql_keywords):
                    issues.append(Issue(
                        file_path=file_path,
                        line_no=node.lineno,
                        column=node.col_offset,
                        rule_id="SEC003",
                        severity="error",
                        message="检测到字符串拼接SQL，存在SQL注入风险",
                        category="security",
                        suggestion="使用参数化查询替代字符串拼接",
                    ))
        return issues

    def _extract_string_concat(self, node: ast.AST) -> str:
        """提取字符串拼接的内容

        Args:
            node: AST节点

        Returns:
            拼接的字符串内容
        """
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            left = self._extract_string_concat(node.left)
            right = self._extract_string_concat(node.right)
            return left + right
        return ""

    def _check_pickle_usage(
        self, tree: ast.AST, file_path: str
    ) -> List[Issue]:
        """检测不安全的pickle使用

        Args:
            tree: AST语法树
            file_path: 文件路径

        Returns:
            问题列表
        """
        issues: List[Issue] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func_name = ""
                if isinstance(node.func, ast.Name):
                    func_name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    func_name = node.func.attr

                if func_name in ("loads", "load"):
                    # 检查是否是pickle的loads/load
                    if isinstance(node.func, ast.Attribute):
                        if isinstance(node.func.value, ast.Name) and node.func.value.id == "pickle":
                            issues.append(Issue(
                                file_path=file_path,
                                line_no=node.lineno,
                                column=node.col_offset,
                                rule_id="SEC004",
                                severity="error",
                                message=f"使用了 pickle.{func_name}()，存在反序列化安全风险",
                                category="security",
                                suggestion="使用更安全的序列化格式如JSON，或限制pickle可加载的类",
                            ))
        return issues

    def _check_assert_for_input(
        self, tree: ast.AST, file_path: str
    ) -> List[Issue]:
        """检测使用assert做输入验证

        Args:
            tree: AST语法树
            file_path: 文件路径

        Returns:
            问题列表
        """
        issues: List[Issue] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Assert):
                # 检查assert是否在函数内（可能用于输入验证）
                issues.append(Issue(
                    file_path=file_path,
                    line_no=node.lineno,
                    column=node.col_offset,
                    rule_id="SEC005",
                    severity="warning",
                    message="使用 assert 进行验证，在优化模式下(-O)会被跳过",
                    category="security",
                    suggestion="使用显式的 if 条件判断和异常替代 assert",
                ))
        return issues
