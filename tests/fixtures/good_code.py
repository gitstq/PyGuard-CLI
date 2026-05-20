"""
良好代码示例 - 用于测试

此文件包含符合最佳实践的Python代码，应产生极少的问题。
"""

import os
import sys
from typing import List, Optional, Dict


class GoodExample:
    """良好代码示例类"""

    def __init__(self, name: str, value: int) -> None:
        """初始化示例

        Args:
            name: 名称
            value: 数值
        """
        self._name: str = name
        self._value: int = value
        self._items: List[str] = []

    def add_item(self, item: str) -> None:
        """添加项目

        Args:
            item: 要添加的项目
        """
        self._items.append(item)

    def get_items(self) -> List[str]:
        """获取所有项目

        Returns:
            项目列表
        """
        return list(self._items)

    def process_data(self, data: Dict[str, int]) -> Optional[int]:
        """处理数据

        Args:
            data: 数据字典

        Returns:
            处理结果，可能为None
        """
        if not data:
            return None

        total = 0
        for key, value in data.items():
            total += value

        return total


def calculate_average(numbers: List[float]) -> float:
    """计算平均值

    Args:
        numbers: 数字列表

    Returns:
        平均值
    """
    if not numbers:
        return 0.0
    return sum(numbers) / len(numbers)


def format_output(title: str, items: List[str]) -> str:
    """格式化输出

    Args:
        title: 标题
        items: 项目列表

    Returns:
        格式化后的字符串
    """
    lines = [f"=== {title} ==="]
    for item in items:
        lines.append(f"  - {item}")
    return "\n".join(lines)


def main() -> int:
    """主函数"""
    example = GoodExample("test", 42)
    example.add_item("item1")
    example.add_item("item2")

    items = example.get_items()
    output = format_output("Items", items)
    print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
