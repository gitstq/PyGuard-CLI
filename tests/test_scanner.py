"""
PyGuard-CLI 扫描引擎单元测试
"""

import os
import sys
import unittest

# 将项目根目录添加到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pyguard.scanner import Scanner, ScanResult
from pyguard.models import Issue
from pyguard.utils import find_python_files, load_config, colorize


class TestScanner(unittest.TestCase):
    """扫描引擎测试类"""

    def setUp(self) -> None:
        """测试前准备"""
        self.scanner = Scanner()
        self.fixtures_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "fixtures"
        )

    def test_scan_good_code(self) -> None:
        """测试扫描良好代码文件"""
        good_file = os.path.join(self.fixtures_dir, "good_code.py")
        result = self.scanner.scan_file(good_file)
        # 良好代码应产生较少问题（允许少量info级别）
        error_count = sum(1 for i in result if i.severity == "error")
        self.assertEqual(error_count, 0, "良好代码不应有error级别问题")

    def test_scan_bad_code(self) -> None:
        """测试扫描不良代码文件"""
        bad_file = os.path.join(self.fixtures_dir, "bad_code.py")
        result = self.scanner.scan_file(bad_file)
        # 不良代码应产生多个问题
        self.assertGreater(len(result), 5, "不良代码应检测到多个问题")

    def test_scan_nonexistent_file(self) -> None:
        """测试扫描不存在的文件"""
        result = self.scanner.scan_file("/nonexistent/file.py")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].rule_id, "SCAN001")

    def test_scan_syntax_error(self) -> None:
        """测试扫描语法错误的文件"""
        import tempfile
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False, encoding="utf-8"
        ) as f:
            f.write("def broken(\n")
            f.flush()
            result = self.scanner.scan_file(f.name)
            os.unlink(f.name)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].rule_id, "SCAN002")

    def test_scan_path(self) -> None:
        """测试扫描目录"""
        result = self.scanner.scan_path(self.fixtures_dir)
        self.assertGreater(result.files_scanned, 0)
        self.assertGreater(result.total_lines, 0)

    def test_scan_empty_dir(self) -> None:
        """测试扫描空目录"""
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            result = self.scanner.scan_path(tmpdir)
            self.assertEqual(result.files_scanned, 0)
            self.assertGreater(len(result.errors), 0)

    def test_check_single_file(self) -> None:
        """测试check_single_file方法"""
        good_file = os.path.join(self.fixtures_dir, "good_code.py")
        result = self.scanner.check_single_file(good_file)
        self.assertEqual(result.files_scanned, 1)

    def test_check_invalid_file(self) -> None:
        """测试检查无效文件"""
        result = self.scanner.check_single_file("/nonexistent/file.py")
        self.assertGreater(len(result.errors), 0)

    def test_result_dataclass(self) -> None:
        """测试ScanResult数据类"""
        result = ScanResult()
        self.assertEqual(result.error_count, 0)
        self.assertEqual(result.warning_count, 0)
        self.assertEqual(result.info_count, 0)

    def test_result_to_dict(self) -> None:
        """测试ScanResult转字典"""
        result = ScanResult()
        d = result.to_dict()
        self.assertIn("issues", d)
        self.assertIn("summary", d)
        self.assertEqual(d["summary"]["total_issues"], 0)

    def test_issue_dataclass(self) -> None:
        """测试Issue数据类"""
        issue = Issue(
            file_path="test.py",
            line_no=1,
            column=0,
            rule_id="TEST001",
            severity="error",
            message="test message",
            category="test",
            suggestion="fix it",
        )
        d = issue.to_dict()
        self.assertEqual(d["file_path"], "test.py")
        self.assertEqual(d["rule_id"], "TEST001")
        self.assertEqual(d["suggestion"], "fix it")


class TestUtils(unittest.TestCase):
    """工具函数测试类"""

    def test_find_python_files(self) -> None:
        """测试查找Python文件"""
        fixtures_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "fixtures"
        )
        files = find_python_files(fixtures_dir)
        self.assertGreater(len(files), 0)
        self.assertTrue(all(f.endswith(".py") for f in files))

    def test_find_python_files_single(self) -> None:
        """测试查找单个Python文件"""
        good_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "fixtures", "good_code.py",
        )
        files = find_python_files(good_file)
        self.assertEqual(len(files), 1)

    def test_find_python_files_non_py(self) -> None:
        """测试查找非Python文件"""
        import tempfile
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False
        ) as f:
            f.write("hello")
            files = find_python_files(f.name)
            os.unlink(f.name)
        self.assertEqual(len(files), 0)

    def test_load_config_default(self) -> None:
        """测试加载默认配置"""
        config = load_config(None)
        self.assertEqual(config["max_line_length"], 120)
        self.assertEqual(config["max_complexity"], 10)

    def test_colorize(self) -> None:
        """测试颜色化函数"""
        result = colorize("test", "\033[31m")
        self.assertIn("test", result)

    def test_severity_to_color(self) -> None:
        """测试严重级别颜色映射"""
        from pyguard.utils import severity_to_color
        self.assertIsNotNone(severity_to_color("error"))
        self.assertIsNotNone(severity_to_color("warning"))
        self.assertIsNotNone(severity_to_color("info"))


if __name__ == "__main__":
    unittest.main()
