"""
不良代码示例 - 用于测试

此文件包含各种代码质量问题，用于验证检测规则的有效性。
"""

import pickle
import os
import json
import sys


# BP002: 可变默认参数
def bad_function(data, items=[]):
    result = ""
    for item in items:
        result += str(item)
    return result


# SEC001: 使用eval
def dangerous_eval(user_input):
    return eval(user_input)


# SEC001: 使用exec
def dangerous_exec(code_str):
    exec(code_str)


# SEC002: 硬编码密码
API_KEY = "sk-1234567890abcdef1234567890abcdef"
password = "my_secret_password_123"


# SEC003: SQL注入风险
def query_user(user_id):
    query = "SELECT * FROM users WHERE id = " + str(user_id)
    return query


# SEC004: 不安全的pickle
def load_data(data_bytes):
    return pickle.loads(data_bytes)


# SEC005: assert做输入验证
def divide(a, b):
    assert b != 0, "Division by zero"
    return a / b


# BP001: 裸except
def unsafe_operation():
    try:
        result = 1 / 0
    except:
        pass
    return None


# TYPE001: 缺少返回类型
def no_return_type(x, y):
    return x + y


# TYPE003: 缺少参数类型
def no_param_type(a, b):
    return a * b


# TYPE002: 使用Any类型
from typing import Any


def use_any_type(data: Any) -> Any:
    return data


# CPLX002: 函数过长
def very_long_function():
    a = 1
    b = 2
    c = 3
    d = 4
    e = 5
    f = 6
    g = 7
    h = 8
    i = 9
    j = 10
    k = 11
    l = 12
    m = 13
    n = 14
    o = 15
    p = 16
    q = 17
    r = 18
    s = 19
    t = 20
    u = 21
    v = 22
    w = 23
    x = 24
    y = 25
    z = 26
    aa = 27
    bb = 28
    cc = 29
    dd = 30
    ee = 31
    ff = 32
    gg = 33
    hh = 34
    ii = 35
    jj = 36
    kk = 37
    ll = 38
    mm = 39
    nn = 40
    oo = 41
    pp = 42
    qq = 43
    rr = 44
    ss = 45
    tt = 46
    uu = 47
    vv = 48
    ww = 49
    xx = 50
    return xx


# CPLX003: 嵌套层级过深
def deeply_nested(data):
    if data:
        if isinstance(data, list):
            for item in data:
                if item:
                    if isinstance(item, dict):
                        for key, value in item.items():
                            if value:
                                return value
    return None


# CPLX004: 参数过多
def too_many_params(a, b, c, d, e, f, g, h, i):
    return a + b + c + d + e + f + g + h + i


# STYLE004: 类名不符合PascalCase
class bad_class_name:
    pass


# STYLE005: 函数名不符合snake_case
def BadFunctionName():
    pass


# BP003: 未使用的导入
import re
import math


# BP004: 未使用的变量
def unused_variables():
    unused_var = 42
    another_unused = "hello"
    return 1


# BP005: 缺少__init__
class NoInitClass:
    def do_something(self):
        return "done"


# PERF001: 循环中字符串拼接
def slow_concat(items):
    result = ""
    for item in items:
        result += str(item)
    return result


# PERF004: 多个字符串+连接
def multi_plus_concat():
    return "a" + "b" + "c" + "d" + "e"


# STYLE001: 行过长
def this_function_has_a_very_very_very_very_very_very_very_very_very_very_very_very_very_long_name_that_exceeds_the_default_line_length_limit_of_120_characters():
    pass
