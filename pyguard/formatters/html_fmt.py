"""
HTML报告格式化器

将扫描结果格式化为带样式的HTML报告。
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..scanner import ScanResult

from .base import BaseFormatter


class HtmlFormatter(BaseFormatter):
    """HTML格式化器"""

    def format(self, result: "ScanResult") -> str:
        """格式化为HTML报告

        Args:
            result: 扫描结果

        Returns:
            HTML字符串
        """
        severity_colors = {
            "error": "#e74c3c",
            "warning": "#f39c12",
            "info": "#3498db",
        }

        issues_rows = ""
        for issue in result.issues:
            color = severity_colors.get(issue.severity, "#95a5a6")
            suggestion_cell = ""
            if issue.suggestion:
                suggestion_cell = f"<td>{issue.suggestion}</td>"
            issues_rows += f"""
            <tr>
                <td><span style="color:{color};font-weight:bold;">[{issue.severity.upper()}]</span></td>
                <td><code>{issue.rule_id}</code></td>
                <td>{issue.file_path}</td>
                <td>{issue.line_no}:{issue.column}</td>
                <td>{issue.message}</td>
                {suggestion_cell}
            </tr>"""

        # 分类统计
        category_counts: dict = {}
        for issue in result.issues:
            cat = issue.category
            category_counts[cat] = category_counts.get(cat, 0) + 1

        category_rows = ""
        category_names = {
            "type": "类型检查",
            "style": "代码风格",
            "security": "安全检测",
            "complexity": "复杂度分析",
            "performance": "性能建议",
            "best_practice": "最佳实践",
            "scanner": "扫描错误",
        }
        for cat, count in sorted(category_counts.items()):
            name = category_names.get(cat, cat)
            category_rows += f"""
            <tr>
                <td>{name}</td>
                <td>{count}</td>
            </tr>"""

        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PyGuard-CLI 代码质量报告</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
               background: #f5f6fa; color: #2c3e50; padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{ text-align: center; padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
               color: white; border-radius: 12px; margin-bottom: 20px; }}
        h2 {{ color: #2c3e50; margin: 20px 0 10px; padding-bottom: 8px;
               border-bottom: 2px solid #667eea; }}
        .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 15px; margin-bottom: 20px; }}
        .card {{ background: white; padding: 20px; border-radius: 10px;
                 box-shadow: 0 2px 10px rgba(0,0,0,0.08); text-align: center; }}
        .card .number {{ font-size: 2em; font-weight: bold; }}
        .card .label {{ color: #7f8c8d; font-size: 0.9em; margin-top: 5px; }}
        .card.error .number {{ color: #e74c3c; }}
        .card.warning .number {{ color: #f39c12; }}
        .card.info .number {{ color: #3498db; }}
        .card.total .number {{ color: #2c3e50; }}
        table {{ width: 100%; border-collapse: collapse; background: white;
                border-radius: 10px; overflow: hidden;
                box-shadow: 0 2px 10px rgba(0,0,0,0.08); margin-bottom: 20px; }}
        th {{ background: #667eea; color: white; padding: 12px 15px; text-align: left; }}
        td {{ padding: 10px 15px; border-bottom: 1px solid #ecf0f1; }}
        tr:hover {{ background: #f8f9fa; }}
        code {{ background: #ecf0f1; padding: 2px 6px; border-radius: 4px; font-size: 0.9em; }}
        .footer {{ text-align: center; color: #95a5a6; margin-top: 30px; padding: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>PyGuard-CLI 代码质量报告</h1>

        <div class="summary">
            <div class="card total">
                <div class="number">{result.files_scanned}</div>
                <div class="label">扫描文件数</div>
            </div>
            <div class="card error">
                <div class="number">{result.error_count}</div>
                <div class="label">错误</div>
            </div>
            <div class="card warning">
                <div class="number">{result.warning_count}</div>
                <div class="label">警告</div>
            </div>
            <div class="card info">
                <div class="number">{result.info_count}</div>
                <div class="label">信息</div>
            </div>
            <div class="card total">
                <div class="number">{result.total_lines}</div>
                <div class="label">代码行数</div>
            </div>
            <div class="card total">
                <div class="number">{result.scan_time:.3f}s</div>
                <div class="label">扫描耗时</div>
            </div>
        </div>

        <h2>问题分类统计</h2>
        <table>
            <thead><tr><th>分类</th><th>数量</th></tr></thead>
            <tbody>{category_rows}</tbody>
        </table>

        <h2>问题详情 ({len(result.issues)})</h2>
        <table>
            <thead>
                <tr>
                    <th>级别</th><th>规则</th><th>文件</th><th>位置</th>
                    <th>描述</th><th>建议</th>
                </tr>
            </thead>
            <tbody>{issues_rows}</tbody>
        </table>

        <div class="footer">
            <p>Generated by PyGuard-CLI v1.0.0</p>
        </div>
    </div>
</body>
</html>"""
        return html
