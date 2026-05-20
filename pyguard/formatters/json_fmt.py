"""
JSON输出格式化器

将扫描结果格式化为结构化的JSON输出。
"""

import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..scanner import ScanResult

from .base import BaseFormatter


class JsonFormatter(BaseFormatter):
    """JSON格式化器"""

    def format(self, result: "ScanResult") -> str:
        """格式化为JSON输出

        Args:
            result: 扫描结果

        Returns:
            JSON字符串
        """
        return json.dumps(result.to_dict(), ensure_ascii=False, indent=2)
