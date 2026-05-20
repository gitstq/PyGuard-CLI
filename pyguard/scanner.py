"""
PyGuard-CLI 核心扫描引擎

负责递归扫描Python文件，使用AST模块解析代码，收集所有规则的检查结果，
生成统计报告。支持并行扫描。
"""

import ast
import os
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Type

from .models import Issue, BaseRule
from .utils import find_python_files, count_lines


@dataclass
class ScanResult:
    """扫描结果数据类"""
    issues: List[Issue] = field(default_factory=list)
    files_scanned: int = 0
    files_with_issues: int = 0
    total_lines: int = 0
    scan_time: float = 0.0
    errors: List[str] = field(default_factory=list)

    @property
    def error_count(self) -> int:
        """error级别问题数"""
        return sum(1 for i in self.issues if i.severity == "error")

    @property
    def warning_count(self) -> int:
        """warning级别问题数"""
        return sum(1 for i in self.issues if i.severity == "warning")

    @property
    def info_count(self) -> int:
        """info级别问题数"""
        return sum(1 for i in self.issues if i.severity == "info")

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "issues": [i.to_dict() for i in self.issues],
            "summary": {
                "files_scanned": self.files_scanned,
                "files_with_issues": self.files_with_issues,
                "total_lines": self.total_lines,
                "total_issues": len(self.issues),
                "error_count": self.error_count,
                "warning_count": self.warning_count,
                "info_count": self.info_count,
                "scan_time": round(self.scan_time, 3),
            },
            "errors": self.errors,
        }


class Scanner:
    """代码扫描引擎

    负责协调所有规则对Python文件进行检查，收集并汇总结果。
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """初始化扫描引擎

        Args:
            config: 配置字典
        """
        self.config: Dict[str, Any] = config or {}
        self._rules: List[BaseRule] = self._init_rules()
        self._ignored_rules: List[str] = self.config.get("ignore_rules", [])

    def _init_rules(self) -> List[BaseRule]:
        """初始化所有检查规则

        Returns:
            规则实例列表
        """
        from .rules.type_checker import TypeChecker
        from .rules.style_checker import StyleChecker
        from .rules.security import SecurityChecker
        from .rules.complexity import ComplexityChecker
        from .rules.performance import PerformanceChecker
        from .rules.best_practices import BestPracticesChecker

        return [
            TypeChecker(self.config),
            StyleChecker(self.config),
            SecurityChecker(self.config),
            ComplexityChecker(self.config),
            PerformanceChecker(self.config),
            BestPracticesChecker(self.config),
        ]

    def _get_active_rules(self) -> List[BaseRule]:
        """获取未被忽略的活跃规则

        Returns:
            活跃规则列表
        """
        return [r for r in self._rules if r.rule_id not in self._ignored_rules]

    def _is_rule_ignored(self, rule_id: str) -> bool:
        """检查规则是否被忽略

        支持忽略整个类别（如SEC）或具体规则（如SEC001）。

        Args:
            rule_id: 规则ID（如SEC001）

        Returns:
            是否被忽略
        """
        # 检查具体规则ID
        if rule_id in self._ignored_rules:
            return True
        # 检查类别级别忽略（如SEC -> 忽略所有SEC001, SEC002等）
        category = rule_id[:3] if len(rule_id) > 3 else rule_id
        return category in self._ignored_rules

    def scan_file(self, file_path: str) -> List[Issue]:
        """扫描单个Python文件

        Args:
            file_path: 文件路径

        Returns:
            发现的问题列表
        """
        issues: List[Issue] = []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                source = f.read()
            lines = source.splitlines()
        except (IOError, UnicodeDecodeError) as e:
            return [Issue(
                file_path=file_path,
                line_no=0,
                column=0,
                rule_id="SCAN001",
                severity="error",
                message=f"无法读取文件: {e}",
                category="scanner",
            )]

        try:
            tree = ast.parse(source, filename=file_path)
        except SyntaxError as e:
            return [Issue(
                file_path=file_path,
                line_no=e.lineno or 0,
                column=e.offset or 0,
                rule_id="SCAN002",
                severity="error",
                message=f"语法错误: {e.msg}",
                category="scanner",
            )]

        for rule in self._get_active_rules():
            try:
                rule_issues = rule.check(tree, file_path, lines)
                # 过滤被忽略的具体规则
                rule_issues = [
                    i for i in rule_issues
                    if not self._is_rule_ignored(i.rule_id)
                ]
                issues.extend(rule_issues)
            except Exception as e:
                issues.append(Issue(
                    file_path=file_path,
                    line_no=0,
                    column=0,
                    rule_id="SCAN003",
                    severity="error",
                    message=f"规则 {rule.rule_id} 执行异常: {e}",
                    category="scanner",
                ))

        return issues

    def scan_path(self, path: str, parallel: bool = False) -> ScanResult:
        """扫描指定路径下的所有Python文件

        Args:
            path: 目录或文件路径
            parallel: 是否启用并行扫描

        Returns:
            扫描结果
        """
        import time
        start_time = time.time()

        result = ScanResult()
        py_files = find_python_files(path)

        if not py_files:
            result.errors.append(f"未找到Python文件: {path}")
            result.scan_time = time.time() - start_time
            return result

        result.files_scanned = len(py_files)
        files_with_issues: set = set()

        if parallel and len(py_files) > 1:
            # 并行扫描模式
            with ProcessPoolExecutor(max_workers=min(os.cpu_count() or 4, 8)) as executor:
                future_to_file = {
                    executor.submit(self.scan_file, f): f for f in py_files
                }
                for future in as_completed(future_to_file):
                    file_path = future_to_file[future]
                    try:
                        file_issues = future.result()
                        result.issues.extend(file_issues)
                        if file_issues:
                            files_with_issues.add(file_path)
                        result.total_lines += count_lines(file_path)
                    except Exception as e:
                        result.errors.append(f"扫描 {file_path} 失败: {e}")
        else:
            # 串行扫描模式
            for file_path in py_files:
                file_issues = self.scan_file(file_path)
                result.issues.extend(file_issues)
                if file_issues:
                    files_with_issues.add(file_path)
                result.total_lines += count_lines(file_path)

        result.files_with_issues = len(files_with_issues)
        result.scan_time = time.time() - start_time

        # 按文件路径和行号排序
        result.issues.sort(key=lambda x: (x.file_path, x.line_no, x.column))

        return result

    def check_single_file(self, file_path: str) -> ScanResult:
        """检查单个文件（与scan_path类似，但只处理单个文件）

        Args:
            file_path: 文件路径

        Returns:
            扫描结果
        """
        import time
        start_time = time.time()

        result = ScanResult()
        abs_path = os.path.abspath(file_path)

        if not os.path.isfile(abs_path) or not abs_path.endswith(".py"):
            result.errors.append(f"无效的Python文件: {file_path}")
            result.scan_time = time.time() - start_time
            return result

        result.files_scanned = 1
        file_issues = self.scan_file(abs_path)
        result.issues.extend(file_issues)
        result.files_with_issues = 1 if file_issues else 0
        result.total_lines = count_lines(abs_path)
        result.scan_time = time.time() - start_time

        return result
