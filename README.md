# PyGuard-CLI

轻量级Python代码质量智能巡检引擎。

## 特性

- 零外部依赖，仅使用Python标准库
- 类型检查、代码风格检测、安全漏洞扫描
- 复杂度分析、性能建议、最佳实践检查
- 支持多种输出格式（text/json/html/markdown）
- TUI仪表盘模式
- 并行扫描支持

## 安装

```bash
pip install -e .
```

## 使用

```bash
# 扫描目录
pyguard scan ./src

# 检查单个文件
pyguard check myfile.py

# 指定输出格式
pyguard scan ./src --format json

# 按严重级别过滤
pyguard scan ./src --severity error

# TUI仪表盘模式
pyguard scan ./src --tui

# 查看版本
pyguard --version
```

## 配置

创建 `pyguard.json` 配置文件：

```json
{
    "max_line_length": 120,
    "max_complexity": 10,
    "max_function_length": 50,
    "max_nesting_depth": 4,
    "max_parameters": 7,
    "max_class_length": 500,
    "ignore_rules": ["STYLE001"]
}
```

## License

MIT
