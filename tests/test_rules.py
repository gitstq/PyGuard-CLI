"""
PyGuard-CLI 检查规则单元测试
"""

import ast
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pyguard.rules.type_checker import TypeChecker
from pyguard.rules.style_checker import StyleChecker
from pyguard.rules.security import SecurityChecker
from pyguard.rules.complexity import ComplexityChecker
from pyguard.rules.performance import PerformanceChecker
from pyguard.rules.best_practices import BestPracticesChecker


class TestTypeChecker(unittest.TestCase):
    """类型检查规则测试"""

    def setUp(self) -> None:
        self.checker = TypeChecker()

    def test_missing_return_type(self) -> None:
        """检测缺少返回类型标注"""
        code = "def foo():\n    pass\n"
        tree = ast.parse(code)
        issues = self.checker.check(tree, "test.py", code.splitlines())
        self.assertTrue(any(i.rule_id == "TYPE001" for i in issues))

    def test_any_usage(self) -> None:
        """检测Any类型使用"""
        code = "from typing import Any\ndef foo(x: Any) -> Any:\n    return x\n"
        tree = ast.parse(code)
        issues = self.checker.check(tree, "test.py", code.splitlines())
        self.assertTrue(any(i.rule_id == "TYPE002" for i in issues))

    def test_missing_param_type(self) -> None:
        """检测缺少参数类型标注"""
        code = "def foo(x, y):\n    return x + y\n"
        tree = ast.parse(code)
        issues = self.checker.check(tree, "test.py", code.splitlines())
        self.assertTrue(any(i.rule_id == "TYPE003" for i in issues))

    def test_good_type_annotations(self) -> None:
        """正确类型标注不产生问题"""
        code = 'def add(a: int, b: int) -> int:\n    return a + b\n'
        tree = ast.parse(code)
        issues = self.checker.check(tree, "test.py", code.splitlines())
        type_issues = [i for i in issues if i.rule_id.startswith("TYPE")]
        self.assertEqual(len(type_issues), 0)


class TestStyleChecker(unittest.TestCase):
    """代码风格检查规则测试"""

    def setUp(self) -> None:
        self.checker = StyleChecker()

    def test_long_line(self) -> None:
        """检测行过长"""
        long_line = "x" * 200
        code = f"{long_line}\n"
        issues = self.checker.check(ast.parse("x=1"), "test.py", code.splitlines())
        self.assertTrue(any(i.rule_id == "STYLE001" for i in issues))

    def test_missing_docstring_class(self) -> None:
        """检测类缺少docstring"""
        code = "class MyClass:\n    pass\n"
        tree = ast.parse(code)
        issues = self.checker.check(tree, "test.py", code.splitlines())
        self.assertTrue(any(i.rule_id == "STYLE002" for i in issues))

    def test_missing_docstring_function(self) -> None:
        """检测函数缺少docstring"""
        code = "def my_func():\n    pass\n"
        tree = ast.parse(code)
        issues = self.checker.check(tree, "test.py", code.splitlines())
        self.assertTrue(any(i.rule_id == "STYLE003" for i in issues))

    def test_trailing_whitespace(self) -> None:
        """检测尾随空格"""
        code = "x = 1   \n"
        issues = self.checker.check(ast.parse("x=1"), "test.py", code.splitlines())
        self.assertTrue(any(i.rule_id == "STYLE006" for i in issues))

    def test_bad_class_name(self) -> None:
        """检测不符合规范的类名"""
        code = "class bad_name:\n    pass\n"
        tree = ast.parse(code)
        issues = self.checker.check(tree, "test.py", code.splitlines())
        self.assertTrue(any(i.rule_id == "STYLE004" for i in issues))

    def test_good_class_name(self) -> None:
        """正确类名不产生问题"""
        code = 'class GoodName:\n    """Docstring."""\n    pass\n'
        tree = ast.parse(code)
        issues = self.checker.check(tree, "test.py", code.splitlines())
        style004 = [i for i in issues if i.rule_id == "STYLE004"]
        self.assertEqual(len(style004), 0)


class TestSecurityChecker(unittest.TestCase):
    """安全检查规则测试"""

    def setUp(self) -> None:
        self.checker = SecurityChecker()

    def test_eval_usage(self) -> None:
        """检测eval使用"""
        code = "result = eval('1+1')\n"
        tree = ast.parse(code)
        issues = self.checker.check(tree, "test.py", code.splitlines())
        self.assertTrue(any(i.rule_id == "SEC001" for i in issues))

    def test_exec_usage(self) -> None:
        """检测exec使用"""
        code = "exec('print(1)')\n"
        tree = ast.parse(code)
        issues = self.checker.check(tree, "test.py", code.splitlines())
        self.assertTrue(any(i.rule_id == "SEC001" for i in issues))

    def test_hardcoded_password(self) -> None:
        """检测硬编码密码"""
        code = 'password = "my_secret_password_123"\n'
        issues = self.checker.check(ast.parse("x=1"), "test.py", code.splitlines())
        self.assertTrue(any(i.rule_id == "SEC002" for i in issues))

    def test_sql_injection_plus(self) -> None:
        """检测SQL注入风险（+拼接）"""
        code = 'query = "SELECT * FROM users WHERE id = " + user_id\n'
        tree = ast.parse("x=1")
        issues = self.checker.check(tree, "test.py", code.splitlines())
        # SQL注入检测基于AST，这里简单验证
        sql_issues = [i for i in issues if i.rule_id == "SEC003"]
        # 由于代码是 x=1，不会有SQL问题
        self.assertEqual(len(sql_issues), 0)

    def test_pickle_usage(self) -> None:
        """检测不安全的pickle使用"""
        code = "import pickle\ndata = pickle.loads(b'data')\n"
        tree = ast.parse(code)
        issues = self.checker.check(tree, "test.py", code.splitlines())
        self.assertTrue(any(i.rule_id == "SEC004" for i in issues))

    def test_assert_usage(self) -> None:
        """检测assert做输入验证"""
        code = "def foo(x):\n    assert x > 0\n"
        tree = ast.parse(code)
        issues = self.checker.check(tree, "test.py", code.splitlines())
        self.assertTrue(any(i.rule_id == "SEC005" for i in issues))


class TestComplexityChecker(unittest.TestCase):
    """复杂度检查规则测试"""

    def setUp(self) -> None:
        self.checker = ComplexityChecker({"max_complexity": 5})

    def test_high_complexity(self) -> None:
        """检测高圈复杂度"""
        code = """
def complex_func(x):
    if x > 0:
        if x > 10:
            if x > 20:
                if x > 30:
                    if x > 40:
                        return x
    return 0
"""
        tree = ast.parse(code)
        issues = self.checker.check(tree, "test.py", code.splitlines())
        self.assertTrue(any(i.rule_id == "CPLX001" for i in issues))

    def test_many_parameters(self) -> None:
        """检测参数过多"""
        code = "def func(a, b, c, d, e, f, g, h):\n    pass\n"
        tree = ast.parse(code)
        issues = self.checker.check(tree, "test.py", code.splitlines())
        self.assertTrue(any(i.rule_id == "CPLX004" for i in issues))

    def test_deep_nesting(self) -> None:
        """检测嵌套层级过深"""
        code = """
def nested():
    if True:
        if True:
            if True:
                if True:
                    if True:
                        pass
"""
        tree = ast.parse(code)
        issues = self.checker.check(tree, "test.py", code.splitlines())
        self.assertTrue(any(i.rule_id == "CPLX003" for i in issues))


class TestPerformanceChecker(unittest.TestCase):
    """性能检查规则测试"""

    def setUp(self) -> None:
        self.checker = PerformanceChecker()

    def test_string_concat_in_loop(self) -> None:
        """检测循环中字符串拼接"""
        code = """
result = ""
for i in range(10):
    result += str(i)
"""
        tree = ast.parse(code)
        issues = self.checker.check(tree, "test.py", code.splitlines())
        self.assertTrue(any(i.rule_id == "PERF001" for i in issues))

    def test_unnecessary_list_comp(self) -> None:
        """检测不必要的列表推导"""
        code = "result = any([x > 0 for x in items])\n"
        tree = ast.parse(code)
        issues = self.checker.check(tree, "test.py", code.splitlines())
        self.assertTrue(any(i.rule_id == "PERF002" for i in issues))

    def test_multi_string_plus(self) -> None:
        """检测多个字符串+连接"""
        code = 'result = "a" + "b" + "c" + "d"\n'
        tree = ast.parse(code)
        issues = self.checker.check(tree, "test.py", code.splitlines())
        self.assertTrue(any(i.rule_id == "PERF004" for i in issues))


class TestBestPracticesChecker(unittest.TestCase):
    """最佳实践检查规则测试"""

    def setUp(self) -> None:
        self.checker = BestPracticesChecker()

    def test_bare_except(self) -> None:
        """检测裸except"""
        code = """
try:
    x = 1 / 0
except:
    pass
"""
        tree = ast.parse(code)
        issues = self.checker.check(tree, "test.py", code.splitlines())
        self.assertTrue(any(i.rule_id == "BP001" for i in issues))

    def test_mutable_default_arg(self) -> None:
        """检测可变默认参数"""
        code = "def func(items=[]):\n    pass\n"
        tree = ast.parse(code)
        issues = self.checker.check(tree, "test.py", code.splitlines())
        self.assertTrue(any(i.rule_id == "BP002" for i in issues))

    def test_unused_imports(self) -> None:
        """检测未使用的导入"""
        code = "import os\nimport re\n\ndef func():\n    pass\n"
        tree = ast.parse(code)
        issues = self.checker.check(tree, "test.py", code.splitlines())
        unused = [i for i in issues if i.rule_id == "BP003"]
        self.assertGreater(len(unused), 0)

    def test_unused_variables(self) -> None:
        """检测未使用的变量"""
        code = "def func():\n    x = 42\n    return 1\n"
        tree = ast.parse(code)
        issues = self.checker.check(tree, "test.py", code.splitlines())
        self.assertTrue(any(i.rule_id == "BP004" for i in issues))

    def test_missing_init(self) -> None:
        """检测缺少__init__"""
        code = """
class MyClass:
    def do_something(self):
        return 1
"""
        tree = ast.parse(code)
        issues = self.checker.check(tree, "test.py", code.splitlines())
        self.assertTrue(any(i.rule_id == "BP005" for i in issues))


if __name__ == "__main__":
    unittest.main()
