"""
PyGuard-CLI 核心数据类型

定义Issue和BaseRule等基础类型，避免循环导入。
"""

import ast
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class Issue:
    """代码问题数据类"""
    file_path: str          # 文件路径
    line_no: int            # 行号
    column: int             # 列号
    rule_id: str            # 规则ID
    severity: str           # 严重级别: error/warning/info
    message: str            # 问题描述
    category: str           # 分类: type/style/security/complexity/performance/best_practice
    suggestion: str = ""    # 修复建议

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "file_path": self.file_path,
            "line_no": self.line_no,
            "column": self.column,
            "rule_id": self.rule_id,
            "severity": self.severity,
            "message": self.message,
            "category": self.category,
            "suggestion": self.suggestion,
        }


class BaseRule(ABC):
    """规则基类，所有检查规则必须继承此类"""

    rule_id: str = ""
    description: str = ""
    severity: str = "info"
    category: str = ""

    @abstractmethod
    def check(self, tree: ast.AST, file_path: str, lines: List[str]) -> List[Issue]:
        """检查AST树，返回问题列表

        Args:
            tree: AST语法树
            file_path: 文件路径
            lines: 文件内容按行分割的列表

        Returns:
            发现的问题列表
        """
        raise NotImplementedError
