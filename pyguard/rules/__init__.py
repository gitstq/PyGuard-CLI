"""
PyGuard-CLI 检查规则包

包含类型检查、代码风格、安全检测、复杂度分析、性能建议和最佳实践等规则模块。
"""


def get_all_checkers(config=None):
    """获取所有检查规则实例

    Args:
        config: 配置字典

    Returns:
        规则实例列表
    """
    from .type_checker import TypeChecker
    from .style_checker import StyleChecker
    from .security import SecurityChecker
    from .complexity import ComplexityChecker
    from .performance import PerformanceChecker
    from .best_practices import BestPracticesChecker

    return [
        TypeChecker(config),
        StyleChecker(config),
        SecurityChecker(config),
        ComplexityChecker(config),
        PerformanceChecker(config),
        BestPracticesChecker(config),
    ]
