<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License">
  <img src="https://img.shields.io/badge/Dependencies-0-orange.svg" alt="Zero Dependencies">
  <img src="https://img.shields.io/badge/Rules-30%2B-purple.svg" alt="30+ Rules">
  <img src="https://img.shields.io/badge/Tests-44-brightgreen.svg" alt="44 Tests">
</p>

<p align="center">
  <b>简体中文</b> | <a href="#繁體中文">繁體中文</a> | <a href="#english">English</a>
</p>

---

# PyGuard-CLI

> 轻量级 Python 代码质量智能巡检引擎 -- 零外部依赖，一行命令，全面体检你的代码。

<p align="center">
  <img src="https://img.shields.io/badge/🛡️-类型检查-blue"> <img src="https://img.shields.io/badge/🎨-代码风格-green"> <img src="https://img.shields.io/badge/🔒-安全检测-red"> <img src="https://img.shields.io/badge/🧩-复杂度分析-yellow"> <img src="https://img.shields.io/badge/⚡-性能建议-orange"> <img src="https://img.shields.io/badge/✅-最佳实践-purple">
</p>

---

## 目录

- [项目介绍](#-项目介绍)
- [核心特性](#-核心特性)
- [快速开始](#-快速开始)
  - [环境要求](#环境要求)
  - [安装](#安装)
  - [使用命令](#使用命令)
- [详细使用指南](#-详细使用指南)
  - [CLI 命令全览](#cli-命令全览)
  - [输出格式](#输出格式)
  - [配置文件](#配置文件)
  - [TUI 仪表盘](#tui-仪表盘)
  - [并行扫描](#并行扫描)
  - [作为 Python 库使用](#作为-python-库使用)
  - [CI/CD 集成](#cicd-集成)
- [检查规则分类](#-检查规则分类)
- [设计思路与迭代规划](#-设计思路与迭代规划)
- [打包与部署指南](#-打包与部署指南)
- [贡献指南](#-贡献指南)
- [开源协议](#-开源协议)

---

## 🎉 项目介绍

PyGuard-CLI 是一款面向 Python 开发者的**轻量级代码质量巡检工具**。它不依赖任何第三方库，仅使用 Python 标准库构建，通过 AST（抽象语法树）静态分析技术，对代码进行多维度、全方位的质量检查。

无论你是个人开发者维护小型项目，还是团队协作管理大型代码库，PyGuard-CLI 都能快速融入你的工作流，帮助你：

- 🔍 **发现潜在缺陷** -- 在代码运行前捕获类型错误、安全隐患和逻辑问题
- 📏 **统一代码风格** -- 确保团队成员遵循一致的编码规范
- 📊 **量化代码质量** -- 通过复杂度分析和统计报告，直观了解代码健康状况
- 🚀 **零成本接入** -- 无需安装任何依赖，`pip install` 即可使用

### 为什么选择 PyGuard-CLI？

| 特性 | PyGuard-CLI | Pylint | Flake8 |
|------|-------------|--------|--------|
| 外部依赖 | **零依赖** | 20+ | 10+ |
| 安装大小 | **< 100KB** | ~10MB | ~5MB |
| TUI 仪表盘 | ✅ | ❌ | ❌ |
| HTML 报告 | ✅ | 插件 | 插件 |
| 安全检测 | ✅ 内置 | 部分 | 插件 |
| 并行扫描 | ✅ | ❌ | ❌ |

---

## ✨ 核心特性

- 🛡️ **6 大检查维度，30+ 条规则** -- 类型检查、代码风格、安全检测、复杂度分析、性能建议、最佳实践
- 📦 **零外部依赖** -- 仅使用 Python 标准库（`ast`、`argparse`、`json`、`concurrent.futures` 等），安装即用
- 🖥️ **TUI 交互式仪表盘** -- 纯终端 ANSI 界面，支持键盘导航、问题浏览、统计图表和文件热力图
- 📄 **多格式输出** -- 彩色终端文本、JSON、HTML 报告、Markdown，适配各种场景
- ⚡ **并行扫描引擎** -- 基于 `ProcessPoolExecutor` 的多进程并行，大幅提升大型项目的扫描速度
- 🔧 **灵活配置** -- JSON 配置文件 + 命令行参数，支持按规则 ID 或类别级别忽略规则
- 🧪 **完善的测试** -- 44 个单元测试覆盖所有检查规则，确保检测准确性
- 🎯 **精准定位** -- 每个问题精确到文件、行号、列号，并附带修复建议

---

## 🚀 快速开始

### 环境要求

- **Python** >= 3.8（支持 3.8 / 3.9 / 3.10 / 3.11 / 3.12）
- **操作系统**：Windows / macOS / Linux
- **终端**：支持 ANSI 转义码的终端（TUI 模式需要）

### 安装

```bash
# 克隆项目
git clone https://github.com/your-username/pyguard-cli.git
cd pyguard-cli

# 方式一：使用 pip 安装（推荐）
pip install .

# 方式二：使用 setup.py 安装
python setup.py install

# 方式三：开发模式安装（可编辑模式，修改源码即时生效）
pip install -e .
```

安装完成后，`pyguard` 命令将自动注册到系统 PATH 中。

验证安装：

```bash
pyguard --version
# 输出: pyguard 1.0.0
```

### 使用命令

```bash
# 📁 扫描当前目录下所有 Python 文件
pyguard scan .

# 📄 检查单个文件
pyguard check my_script.py

# 📊 以 JSON 格式输出（便于程序处理）
pyguard scan . --format json

# 🖥️ 启动 TUI 交互式仪表盘
pyguard scan . --tui

# 🔴 只显示错误级别的问题
pyguard scan . --severity error

# 🚀 启用并行扫描加速
pyguard scan . --parallel

# 🙈 忽略指定规则
pyguard scan . --ignore STYLE001 STYLE007

# 📋 使用自定义配置文件
pyguard scan . --config my_pyguard.json

# 📝 输出 HTML 格式报告
pyguard scan . --format html > report.html

# 📑 输出 Markdown 格式报告
pyguard scan . --format markdown > report.md
```

---

## 📖 详细使用指南

### CLI 命令全览

```
pyguard [--version]
pyguard scan <path> [选项]
pyguard check <file> [选项]
```

#### `scan` -- 扫描路径

递归扫描指定目录或文件下的所有 Python 文件，执行全面的质量检查。

```bash
pyguard scan <path> [选项]
```

| 参数 | 缩写 | 说明 | 默认值 |
|------|------|------|--------|
| `--format` | `-f` | 输出格式：`text` / `json` / `html` / `markdown` | `text` |
| `--severity` | `-s` | 严重级别过滤：`error` / `warning` / `info` / `all` | `all` |
| `--ignore` | `-i` | 忽略指定的规则 ID（支持多个） | 无 |
| `--config` | `-c` | 指定配置文件路径 | 自动查找 |
| `--parallel` | `-p` | 启用并行扫描 | 关闭 |
| `--tui` | | 启动 TUI 仪表盘模式 | 关闭 |

#### `check` -- 检查单文件

对单个 Python 文件执行详细的质量检查。

```bash
pyguard check <file> [选项]
```

参数与 `scan` 基本一致（不支持 `--parallel`）。

### 输出格式

#### 彩色终端（text，默认）

默认输出格式，使用 ANSI 颜色高亮不同严重级别的问题：

```
[E] TYPE001  my_script.py:15:3   函数 'process_data' 缺少返回类型标注
[W] STYLE001 my_script.py:42:1   行长度超过限制 (135 > 120)
[I] BP003    my_script.py:3:1    导入 're' 未被使用
```

#### JSON 格式

结构化 JSON 输出，便于与其他工具集成：

```bash
pyguard scan . --format json
```

```json
{
  "issues": [
    {
      "file_path": "/path/to/my_script.py",
      "line_no": 15,
      "column": 3,
      "rule_id": "TYPE001",
      "severity": "error",
      "message": "函数 'process_data' 缺少返回类型标注",
      "category": "type",
      "suggestion": "添加返回类型标注，例如: def process_data(...) -> ReturnType:"
    }
  ],
  "summary": {
    "files_scanned": 12,
    "files_with_issues": 5,
    "total_lines": 1580,
    "total_issues": 23,
    "error_count": 3,
    "warning_count": 12,
    "info_count": 8,
    "scan_time": 0.156
  }
}
```

#### HTML 报告

生成带样式的 HTML 报告，适合团队评审和存档：

```bash
pyguard scan . --format html > report.html
```

HTML 报告包含：统计概览卡片、问题分类统计表、问题详情列表，采用响应式设计，可直接在浏览器中查看。

#### Markdown 格式

生成 Markdown 格式的报告，适合嵌入文档或提交说明：

```bash
pyguard scan . --format markdown > report.md
```

### 配置文件

在项目根目录创建 `pyguard.json` 或 `.pyguard.json` 配置文件，PyGuard-CLI 会自动加载：

```json
{
  "max_line_length": 120,
  "max_complexity": 10,
  "max_function_length": 50,
  "max_nesting_depth": 4,
  "max_parameters": 7,
  "max_class_length": 500,
  "ignore_rules": ["STYLE001", "STYLE007"]
}
```

#### 配置项说明

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `max_line_length` | int | `120` | 单行最大字符数 |
| `max_complexity` | int | `10` | 函数最大圈复杂度 |
| `max_function_length` | int | `50` | 函数最大行数 |
| `max_nesting_depth` | int | `4` | 最大嵌套层级 |
| `max_parameters` | int | `7` | 函数最大参数个数 |
| `max_class_length` | int | `500` | 类最大行数 |
| `ignore_rules` | list | `[]` | 要忽略的规则 ID 列表 |

> 💡 **提示**：命令行参数 `--ignore` 会与配置文件中的 `ignore_rules` 合并，两者取并集。

### TUI 仪表盘

使用 `--tui` 参数启动交互式终端仪表盘：

```bash
pyguard scan . --tui
```

TUI 仪表盘提供三个标签页：

| 标签页 | 功能 |
|--------|------|
| **问题列表** | 浏览所有检测到的问题，上下键选择查看详情 |
| **统计概览** | 查看扫描统计、问题分布图、分类柱状图 |
| **文件热力图** | 按文件维度展示问题密度分布 |

**快捷键：**

| 按键 | 功能 |
|------|------|
| `↑` / `k` | 向上移动选择 |
| `↓` / `j` | 向下移动选择 |
| `Tab` | 切换标签页 |
| `q` / `Ctrl+C` | 退出仪表盘 |

### 并行扫描

对于大型项目，启用并行扫描可显著提升速度：

```bash
pyguard scan . --parallel
```

并行扫描基于 `ProcessPoolExecutor` 实现，自动检测 CPU 核心数（最多使用 8 个工作进程），将文件分配到多个进程中同时分析。

> ⚠️ **注意**：并行模式在文件数量较少（< 10 个）时可能不会带来明显提升，因为进程启动本身有开销。

### 作为 Python 库使用

除了命令行工具，PyGuard-CLI 也可以直接作为 Python 库在代码中调用：

```python
from pyguard.scanner import Scanner

# 初始化扫描器（可传入自定义配置）
scanner = Scanner(config={
    "max_line_length": 100,
    "max_complexity": 8,
})

# 扫描指定路径
result = scanner.scan_path("./my_project")

# 查看结果
print(f"扫描文件数: {result.files_scanned}")
print(f"发现问题数: {len(result.issues)}")
print(f"错误: {result.error_count}")
print(f"警告: {result.warning_count}")
print(f"信息: {result.info_count}")
print(f"扫描耗时: {result.scan_time:.3f}s")

# 遍历问题详情
for issue in result.issues:
    print(f"[{issue.severity}] {issue.rule_id} "
          f"{issue.file_path}:{issue.line_no} - {issue.message}")
    if issue.suggestion:
        print(f"  建议: {issue.suggestion}")

# 检查单个文件
single_result = scanner.check_single_file("./my_script.py")
```

### CI/CD 集成

PyGuard-CLI 的退出码设计便于集成到 CI/CD 流水线：

| 退出码 | 含义 |
|--------|------|
| `0` | 扫描完成，未发现 error 级别问题 |
| `1` | 扫描完成，发现 error 级别问题 |
| `2` | 命令行参数错误或扫描过程出错 |

#### GitHub Actions 示例

```yaml
name: Code Quality Check

on: [push, pull_request]

jobs:
  pyguard:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install PyGuard-CLI
        run: pip install .
      - name: Run PyGuard Scan
        run: pyguard scan . --format json --severity error > pyguard-report.json
      - name: Check Results
        run: |
          if grep -q '"error_count": [1-9]' pyguard-report.json; then
            echo "::error::PyGuard detected errors! Check the report."
            exit 1
          fi
```

#### Git pre-commit Hook 示例

```bash
# .git/hooks/pre-commit
#!/bin/bash
echo "Running PyGuard-CLI..."
pyguard scan . --severity error
if [ $? -ne 0 ]; then
    echo "❌ PyGuard detected errors. Please fix before committing."
    exit 1
fi
echo "✅ PyGuard check passed."
```

---

## 📋 检查规则分类

PyGuard-CLI 内置 **6 大检查维度、30+ 条规则**，覆盖代码质量的方方面面。

### 🛡️ 类型检查 (TYPE001 - TYPE005)

| 规则 ID | 说明 | 级别 |
|---------|------|------|
| TYPE001 | 函数缺少返回类型标注 | warning |
| TYPE002 | 使用 `Any` 类型 | info |
| TYPE003 | 参数缺少类型标注 | info |
| TYPE004 | `Optional` 类型未正确处理 | warning |
| TYPE005 | 类型注解使用字符串而非直接引用 | info |

### 🎨 代码风格 (STYLE001 - STYLE008)

| 规则 ID | 说明 | 级别 |
|---------|------|------|
| STYLE001 | 行长度超过限制 | warning |
| STYLE002 | 函数缺少 docstring | info |
| STYLE003 | 类缺少 docstring | info |
| STYLE004 | 命名不符合规范（类名/函数名/变量名） | warning |
| STYLE005 | 尾随空格 | info |
| STYLE006 | 尾随空行 | info |
| STYLE007 | 导入顺序不规范 | info |
| STYLE008 | 多空行 | info |

### 🔒 安全检测 (SEC001 - SEC005)

| 规则 ID | 说明 | 级别 |
|---------|------|------|
| SEC001 | 使用 `eval()` 或 `exec()` | error |
| SEC002 | 硬编码密码/密钥 | error |
| SEC003 | SQL 注入风险 | error |
| SEC004 | 不安全的 `pickle` 使用 | warning |
| SEC005 | 使用 `assert` 做输入验证 | warning |

### 🧩 复杂度分析 (CPLX001 - CPLX005)

| 规则 ID | 说明 | 级别 |
|---------|------|------|
| CPLX001 | 圈复杂度过高 | warning |
| CPLX002 | 函数过长 | warning |
| CPLX003 | 嵌套层级过深 | warning |
| CPLX004 | 参数过多 | info |
| CPLX005 | 类过大 | info |

### ⚡ 性能建议 (PERF001 - PERF005)

| 规则 ID | 说明 | 级别 |
|---------|------|------|
| PERF001 | 循环中字符串拼接 | info |
| PERF002 | 不必要的列表推导（如 `any([x for x in ...])`） | info |
| PERF003 | 全局变量查找 | info |
| PERF004 | 大量字符串连接 | info |
| PERF005 | 循环中重复调用 | info |

### ✅ 最佳实践 (BP001 - BP005)

| 规则 ID | 说明 | 级别 |
|---------|------|------|
| BP001 | 过于宽泛的异常捕获（裸 `except`） | warning |
| BP002 | 可变默认参数 | warning |
| BP003 | 未使用的导入 | info |
| BP004 | 未使用的变量 | info |
| BP005 | 类缺少 `__init__` 定义 | info |

---

## 💡 设计思路与迭代规划

### 设计理念

PyGuard-CLI 的核心设计哲学是 **"轻量但不简陋"**：

1. **零依赖原则** -- 仅使用 Python 标准库，确保在任何 Python 环境中都能运行，不引入版本冲突风险
2. **AST 静态分析** -- 基于抽象语法树而非正则匹配，保证检测的准确性和可靠性
3. **渐进式使用** -- 开箱即用，无需复杂配置；同时提供丰富的配置选项满足进阶需求
4. **多场景适配** -- CLI 直接使用、Python 库调用、CI/CD 集成、TUI 交互，覆盖各种使用场景

### 架构概览

```
pyguard/
├── cli.py              # CLI 入口，参数解析与命令分发
├── scanner.py          # 核心扫描引擎，协调规则执行
├── models.py           # 数据模型（Issue、BaseRule）
├── utils.py            # 工具函数（颜色、文件查找、配置加载）
├── rules/              # 检查规则模块
│   ├── type_checker.py       # 类型检查规则
│   ├── style_checker.py      # 代码风格规则
│   ├── security.py           # 安全检测规则
│   ├── complexity.py         # 复杂度分析规则
│   ├── performance.py        # 性能建议规则
│   └── best_practices.py     # 最佳实践规则
├── formatters/          # 输出格式化器
│   ├── base.py               # 格式化器基类
│   ├── json_fmt.py           # JSON 格式
│   ├── html_fmt.py           # HTML 报告
│   └── markdown_fmt.py       # Markdown 格式
└── tui/                 # TUI 仪表盘
    └── dashboard.py          # 交互式终端界面
```

### 迭代规划

- [x] **v1.0** -- 核心功能：6 大检查维度、30+ 规则、多格式输出、TUI 仪表盘、并行扫描
- [ ] **v1.1** -- 增量扫描：只检查变更的文件，支持 Git diff 集成
- [ ] **v1.2** -- 自动修复：对部分规则提供 `--fix` 自动修复功能
- [ ] **v1.3** -- 插件系统：支持用户自定义检查规则
- [ ] **v2.0** -- 类型推断引擎：基于控制流分析的跨函数类型推断

---

## 📦 打包与部署指南

### 本地安装

```bash
# 进入项目目录
cd pyguard-cli

# 安装到当前 Python 环境
pip install .

# 开发模式安装（推荐贡献者使用）
pip install -e .
```

### 构建分发包

```bash
# 安装构建工具
pip install build

# 构建 sdist 和 wheel
python -m build

# 构建产物位于 dist/ 目录
ls dist/
# pyguard_cli-1.0.0-py3-none-any.whl
# pyguard-cli-1.0.0.tar.gz
```

### 安装到指定环境

```bash
# 从 wheel 安装
pip install dist/pyguard_cli-1.0.0-py3-none-any.whl

# 从源码包安装
pip install dist/pyguard-cli-1.0.0.tar.gz
```

### Docker 部署

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .
RUN pip install .

# 扫描挂载的代码目录
ENTRYPOINT ["pyguard"]
CMD ["scan", "/code"]
```

```bash
# 构建镜像
docker build -t pyguard-cli .

# 扫描本地项目
docker run --rm -v $(pwd):/code pyguard-cli scan /code --format json
```

### 离线部署

由于 PyGuard-CLI 零外部依赖，可以直接将源码复制到目标环境安装：

```bash
# 在有网络的机器上
tar czf pyguard-cli.tar.gz pyguard-cli/

# 传输到离线环境后
tar xzf pyguard-cli.tar.gz
cd pyguard-cli
pip install . --no-index --no-deps
```

---

## 🤝 贡献指南

我们欢迎并感谢所有形式的贡献！无论是提交 Bug 报告、改进建议，还是直接提交代码。

### 如何贡献

1. **Fork** 本仓库
2. 创建特性分支：`git checkout -b feature/my-new-feature`
3. 编写代码并确保通过所有测试：`python -m pytest tests/`
4. 提交变更：`git commit -m "feat: add some awesome feature"`
5. 推送分支：`git push origin feature/my-new-feature`
6. 提交 **Pull Request**

### 开发环境搭建

```bash
# 克隆仓库
git clone https://github.com/your-username/pyguard-cli.git
cd pyguard-cli

# 开发模式安装
pip install -e .

# 运行测试
python -m pytest tests/ -v

# 运行特定测试
python -m pytest tests/test_rules.py -v
python -m pytest tests/test_scanner.py -v
```

### 代码规范

- 所有代码文件使用 **UTF-8** 编码
- 遵循 **PEP 8** 编码规范
- 所有公开函数和类必须包含 **docstring**
- 新增规则必须附带对应的 **单元测试**
- 提交信息遵循 **Conventional Commits** 规范

### 提交规范

```
feat: 新增 XXX 规则
fix: 修复 XXX 规则的误报问题
docs: 更新 README 文档
test: 新增 XXX 规则的单元测试
refactor: 重构 XXX 模块
```

---

## 📄 开源协议

本项目基于 [MIT License](LICENSE) 开源。

```
MIT License

Copyright (c) 2024 PyGuard Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

---

<p align="center">
  Made with ❤️ by <strong>PyGuard Team</strong>
</p>

---
---

<p align="center">
  <a href="#pyguard-cli">简体中文</a> | <b>繁體中文</b> | <a href="#english">English</a>
</p>

---

# PyGuard-CLI

> 輕量級 Python 程式碼品質智慧巡檢引擎 -- 零外部依賴，一行指令，全面體檢你的程式碼。

<p align="center">
  <img src="https://img.shields.io/badge/🛡️-類型檢查-blue"> <img src="https://img.shields.io/badge/🎨-程式碼風格-green"> <img src="https://img.shields.io/badge/🔒-安全偵測-red"> <img src="https://img.shields.io/badge/🧩-複雜度分析-yellow"> <img src="https://img.shields.io/badge/⚡-效能建議-orange"> <img src="https://img.shields.io/badge/✅-最佳實踐-purple">
</p>

---

## 目錄

- [專案介紹](#-專案介紹-1)
- [核心特性](#-核心特性-1)
- [快速開始](#-快速開始-1)
  - [環境需求](#環境需求)
  - [安裝](#安裝-1)
  - [使用指令](#使用指令)
- [詳細使用指南](#-詳細使用指南-1)
  - [CLI 指令全覽](#cli-指令全覽)
  - [輸出格式](#輸出格式-1)
  - [設定檔](#設定檔)
  - [TUI 儀表板](#tui-儀表板)
  - [平行掃描](#平行掃描)
  - [作為 Python 函式庫使用](#作為-python-函式庫使用)
  - [CI/CD 整合](#cicd-整合)
- [檢查規則分類](#-檢查規則分類-1)
- [設計思路與迭代規劃](#-設計思路與迭代規劃-1)
- [打包與部署指南](#-打包與部署指南-1)
- [貢獻指南](#-貢獻指南-1)
- [開源協議](#-開源協議-1)

---

## 🎉 專案介紹

PyGuard-CLI 是一款面向 Python 開發者的**輕量級程式碼品質巡檢工具**。它不依賴任何第三方函式庫，僅使用 Python 標準函式庫建構，透過 AST（抽象語法樹）靜態分析技術，對程式碼進行多維度、全方位的品質檢查。

無論你是個人開發者維護小型專案，還是團隊協作管理大型程式碼庫，PyGuard-CLI 都能快速融入你的工作流程，幫助你：

- 🔍 **發現潛在缺陷** -- 在程式碼執行前捕捉類型錯誤、安全隱患和邏輯問題
- 📏 **統一程式碼風格** -- 確保團隊成員遵循一致的編碼規範
- 📊 **量化程式碼品質** -- 透過複雜度分析和統計報告，直觀了解程式碼健康狀況
- 🚀 **零成本接入** -- 無需安裝任何依賴，`pip install` 即可使用

### 為什麼選擇 PyGuard-CLI？

| 特性 | PyGuard-CLI | Pylint | Flake8 |
|------|-------------|--------|--------|
| 外部依賴 | **零依賴** | 20+ | 10+ |
| 安裝大小 | **< 100KB** | ~10MB | ~5MB |
| TUI 儀表板 | ✅ | ❌ | ❌ |
| HTML 報告 | ✅ | 外掛 | 外掛 |
| 安全偵測 | ✅ 內建 | 部分 | 外掛 |
| 平行掃描 | ✅ | ❌ | ❌ |

---

## ✨ 核心特性

- 🛡️ **6 大檢查維度，30+ 條規則** -- 類型檢查、程式碼風格、安全偵測、複雜度分析、效能建議、最佳實踐
- 📦 **零外部依賴** -- 僅使用 Python 標準函式庫（`ast`、`argparse`、`json`、`concurrent.futures` 等），安裝即用
- 🖥️ **TUI 互動式儀表板** -- 純終端 ANSI 介面，支援鍵盤導航、問題瀏覽、統計圖表和檔案熱力圖
- 📄 **多格式輸出** -- 彩色終端文字、JSON、HTML 報告、Markdown，適配各種場景
- ⚡ **平行掃描引擎** -- 基於 `ProcessPoolExecutor` 的多程序平行，大幅提升大型專案的掃描速度
- 🔧 **靈活設定** -- JSON 設定檔 + 命令列參數，支援按規則 ID 或類別層級忽略規則
- 🧪 **完善的測試** -- 44 個單元測試覆蓋所有檢查規則，確保偵測準確性
- 🎯 **精準定位** -- 每個問題精確到檔案、行號、列號，並附帶修復建議

---

## 🚀 快速開始

### 環境需求

- **Python** >= 3.8（支援 3.8 / 3.9 / 3.10 / 3.11 / 3.12）
- **作業系統**：Windows / macOS / Linux
- **終端**：支援 ANSI 跳脫碼的終端（TUI 模式需要）

### 安裝

```bash
# 克隆專案
git clone https://github.com/your-username/pyguard-cli.git
cd pyguard-cli

# 方式一：使用 pip 安裝（推薦）
pip install .

# 方式二：使用 setup.py 安裝
python setup.py install

# 方式三：開發模式安裝（可編輯模式，修改原始碼即時生效）
pip install -e .
```

安裝完成後，`pyguard` 指令將自動註冊到系統 PATH 中。

驗證安裝：

```bash
pyguard --version
# 輸出: pyguard 1.0.0
```

### 使用指令

```bash
# 📁 掃描目前目錄下所有 Python 檔案
pyguard scan .

# 📄 檢查單一檔案
pyguard check my_script.py

# 📊 以 JSON 格式輸出（便於程式處理）
pyguard scan . --format json

# 🖥️ 啟動 TUI 互動式儀表板
pyguard scan . --tui

# 🔴 只顯示錯誤級別的問題
pyguard scan . --severity error

# 🚀 啟用平行掃描加速
pyguard scan . --parallel

# 🙈 忽略指定規則
pyguard scan . --ignore STYLE001 STYLE007

# 📋 使用自訂設定檔
pyguard scan . --config my_pyguard.json

# 📝 輸出 HTML 格式報告
pyguard scan . --format html > report.html

# 📑 輸出 Markdown 格式報告
pyguard scan . --format markdown > report.md
```

---

## 📖 詳細使用指南

### CLI 指令全覽

```
pyguard [--version]
pyguard scan <path> [選項]
pyguard check <file> [選項]
```

#### `scan` -- 掃描路徑

遞迴掃描指定目錄或檔案下的所有 Python 檔案，執行全面的品質檢查。

```bash
pyguard scan <path> [選項]
```

| 參數 | 縮寫 | 說明 | 預設值 |
|------|------|------|--------|
| `--format` | `-f` | 輸出格式：`text` / `json` / `html` / `markdown` | `text` |
| `--severity` | `-s` | 嚴重級別過濾：`error` / `warning` / `info` / `all` | `all` |
| `--ignore` | `-i` | 忽略指定的規則 ID（支援多個） | 無 |
| `--config` | `-c` | 指定設定檔路徑 | 自動尋找 |
| `--parallel` | `-p` | 啟用平行掃描 | 關閉 |
| `--tui` | | 啟動 TUI 儀表板模式 | 關閉 |

#### `check` -- 檢查單檔案

對單一 Python 檔案執行詳細的品質檢查。

```bash
pyguard check <file> [選項]
```

參數與 `scan` 基本一致（不支援 `--parallel`）。

### 輸出格式

#### 彩色終端（text，預設）

預設輸出格式，使用 ANSI 顏色標記不同嚴重級別的問題：

```
[E] TYPE001  my_script.py:15:3   函式 'process_data' 缺少回傳類型標註
[W] STYLE001 my_script.py:42:1   行長度超過限制 (135 > 120)
[I] BP003    my_script.py:3:1    匯入 're' 未被使用
```

#### JSON 格式

結構化 JSON 輸出，便於與其他工具整合：

```bash
pyguard scan . --format json
```

```json
{
  "issues": [
    {
      "file_path": "/path/to/my_script.py",
      "line_no": 15,
      "column": 3,
      "rule_id": "TYPE001",
      "severity": "error",
      "message": "函式 'process_data' 缺少回傳類型標註",
      "category": "type",
      "suggestion": "新增回傳類型標註，例如: def process_data(...) -> ReturnType:"
    }
  ],
  "summary": {
    "files_scanned": 12,
    "files_with_issues": 5,
    "total_lines": 1580,
    "total_issues": 23,
    "error_count": 3,
    "warning_count": 12,
    "info_count": 8,
    "scan_time": 0.156
  }
}
```

#### HTML 報告

產生帶樣式的 HTML 報告，適合團隊審查和存檔：

```bash
pyguard scan . --format html > report.html
```

HTML 報告包含：統計概覽卡片、問題分類統計表、問題詳情列表，採用響應式設計，可直接在瀏覽器中檢視。

#### Markdown 格式

產生 Markdown 格式的報告，適合嵌入文件或提交說明：

```bash
pyguard scan . --format markdown > report.md
```

### 設定檔

在專案根目錄建立 `pyguard.json` 或 `.pyguard.json` 設定檔，PyGuard-CLI 會自動載入：

```json
{
  "max_line_length": 120,
  "max_complexity": 10,
  "max_function_length": 50,
  "max_nesting_depth": 4,
  "max_parameters": 7,
  "max_class_length": 500,
  "ignore_rules": ["STYLE001", "STYLE007"]
}
```

#### 設定項說明

| 設定項 | 類型 | 預設值 | 說明 |
|--------|------|--------|------|
| `max_line_length` | int | `120` | 單行最大字元數 |
| `max_complexity` | int | `10` | 函式最大圈複雜度 |
| `max_function_length` | int | `50` | 函式最大行數 |
| `max_nesting_depth` | int | `4` | 最大巢狀層級 |
| `max_parameters` | int | `7` | 函式最大參數個數 |
| `max_class_length` | int | `500` | 類別最大行數 |
| `ignore_rules` | list | `[]` | 要忽略的規則 ID 列表 |

> 💡 **提示**：命令列參數 `--ignore` 會與設定檔中的 `ignore_rules` 合併，兩者取聯集。

### TUI 儀表板

使用 `--tui` 參數啟動互動式終端儀表板：

```bash
pyguard scan . --tui
```

TUI 儀表板提供三個分頁：

| 分頁 | 功能 |
|------|------|
| **問題列表** | 瀏覽所有偵測到的問題，上下鍵選擇檢視詳情 |
| **統計概覽** | 檢視掃描統計、問題分佈圖、分類長條圖 |
| **檔案熱力圖** | 按檔案維度展示問題密度分佈 |

**快速鍵：**

| 按鍵 | 功能 |
|------|------|
| `↑` / `k` | 向上移動選擇 |
| `↓` / `j` | 向下移動選擇 |
| `Tab` | 切換分頁 |
| `q` / `Ctrl+C` | 退出儀表板 |

### 平行掃描

對於大型專案，啟用平行掃描可顯著提升速度：

```bash
pyguard scan . --parallel
```

平行掃描基於 `ProcessPoolExecutor` 實作，自動偵測 CPU 核心數（最多使用 8 個工作程序），將檔案分配到多個程序中同時分析。

> ⚠️ **注意**：平行模式在檔案數量較少（< 10 個）時可能不會帶來明顯提升，因為程序啟動本身有開銷。

### 作為 Python 函式庫使用

除了命令列工具，PyGuard-CLI 也可以直接作為 Python 函式庫在程式碼中呼叫：

```python
from pyguard.scanner import Scanner

# 初始化掃描器（可傳入自訂設定）
scanner = Scanner(config={
    "max_line_length": 100,
    "max_complexity": 8,
})

# 掃描指定路徑
result = scanner.scan_path("./my_project")

# 檢視結果
print(f"掃描檔案數: {result.files_scanned}")
print(f"發現問題數: {len(result.issues)}")
print(f"錯誤: {result.error_count}")
print(f"警告: {result.warning_count}")
print(f"資訊: {result.info_count}")
print(f"掃描耗時: {result.scan_time:.3f}s")

# 遍歷問題詳情
for issue in result.issues:
    print(f"[{issue.severity}] {issue.rule_id} "
          f"{issue.file_path}:{issue.line_no} - {issue.message}")
    if issue.suggestion:
        print(f"  建議: {issue.suggestion}")

# 檢查單一檔案
single_result = scanner.check_single_file("./my_script.py")
```

### CI/CD 整合

PyGuard-CLI 的結束碼設計便於整合到 CI/CD 流水線：

| 結束碼 | 含義 |
|--------|------|
| `0` | 掃描完成，未發現 error 級別問題 |
| `1` | 掃描完成，發現 error 級別問題 |
| `2` | 命令列參數錯誤或掃描過程出錯 |

#### GitHub Actions 範例

```yaml
name: Code Quality Check

on: [push, pull_request]

jobs:
  pyguard:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install PyGuard-CLI
        run: pip install .
      - name: Run PyGuard Scan
        run: pyguard scan . --format json --severity error > pyguard-report.json
      - name: Check Results
        run: |
          if grep -q '"error_count": [1-9]' pyguard-report.json; then
            echo "::error::PyGuard detected errors! Check the report."
            exit 1
          fi
```

#### Git pre-commit Hook 範例

```bash
# .git/hooks/pre-commit
#!/bin/bash
echo "Running PyGuard-CLI..."
pyguard scan . --severity error
if [ $? -ne 0 ]; then
    echo "❌ PyGuard detected errors. Please fix before committing."
    exit 1
fi
echo "✅ PyGuard check passed."
```

---

## 📋 檢查規則分類

PyGuard-CLI 內建 **6 大檢查維度、30+ 條規則**，覆蓋程式碼品質的方方面面。

### 🛡️ 類型檢查 (TYPE001 - TYPE005)

| 規則 ID | 說明 | 級別 |
|---------|------|------|
| TYPE001 | 函式缺少回傳類型標註 | warning |
| TYPE002 | 使用 `Any` 類型 | info |
| TYPE003 | 參數缺少類型標註 | info |
| TYPE004 | `Optional` 類型未正確處理 | warning |
| TYPE005 | 類型標註使用字串而非直接引用 | info |

### 🎨 程式碼風格 (STYLE001 - STYLE008)

| 規則 ID | 說明 | 級別 |
|---------|------|------|
| STYLE001 | 行長度超過限制 | warning |
| STYLE002 | 函式缺少 docstring | info |
| STYLE003 | 類別缺少 docstring | info |
| STYLE004 | 命名不符合規範（類別名/函式名/變數名） | warning |
| STYLE005 | 尾隨空格 | info |
| STYLE006 | 尾隨空行 | info |
| STYLE007 | 匯入順序不規範 | info |
| STYLE008 | 多空行 | info |

### 🔒 安全偵測 (SEC001 - SEC005)

| 規則 ID | 說明 | 級別 |
|---------|------|------|
| SEC001 | 使用 `eval()` 或 `exec()` | error |
| SEC002 | 硬編碼密碼/金鑰 | error |
| SEC003 | SQL 注入風險 | error |
| SEC004 | 不安全的 `pickle` 使用 | warning |
| SEC005 | 使用 `assert` 做輸入驗證 | warning |

### 🧩 複雜度分析 (CPLX001 - CPLX005)

| 規則 ID | 說明 | 級別 |
|---------|------|------|
| CPLX001 | 圈複雜度過高 | warning |
| CPLX002 | 函式過長 | warning |
| CPLX003 | 巢狀層級過深 | warning |
| CPLX004 | 參數過多 | info |
| CPLX005 | 類別過大 | info |

### ⚡ 效能建議 (PERF001 - PERF005)

| 規則 ID | 說明 | 級別 |
|---------|------|------|
| PERF001 | 迴圈中字串拼接 | info |
| PERF002 | 不必要的列表推導（如 `any([x for x in ...])`） | info |
| PERF003 | 全域變數查找 | info |
| PERF004 | 大量字串連接 | info |
| PERF005 | 迴圈中重複呼叫 | info |

### ✅ 最佳實踐 (BP001 - BP005)

| 規則 ID | 說明 | 級別 |
|---------|------|------|
| BP001 | 過於寬泛的例外捕捉（裸 `except`） | warning |
| BP002 | 可變預設參數 | warning |
| BP003 | 未使用的匯入 | info |
| BP004 | 未使用的變數 | info |
| BP005 | 類別缺少 `__init__` 定義 | info |

---

## 💡 設計思路與迭代規劃

### 設計理念

PyGuard-CLI 的核心設計哲學是 **「輕量但不簡陋」**：

1. **零依賴原則** -- 僅使用 Python 標準函式庫，確保在任何 Python 環境中都能執行，不引入版本衝突風險
2. **AST 靜態分析** -- 基於抽象語法樹而非正規表示式匹配，保證偵測的準確性和可靠性
3. **漸進式使用** -- 開箱即用，無需複雜設定；同時提供豐富的設定選項滿足進階需求
4. **多場景適配** -- CLI 直接使用、Python 函式庫呼叫、CI/CD 整合、TUI 互動，覆蓋各種使用場景

### 架構概覽

```
pyguard/
├── cli.py              # CLI 入口，參數解析與指令分發
├── scanner.py          # 核心掃描引擎，協調規則執行
├── models.py           # 資料模型（Issue、BaseRule）
├── utils.py            # 工具函式（顏色、檔案尋找、設定載入）
├── rules/              # 檢查規則模組
│   ├── type_checker.py       # 類型檢查規則
│   ├── style_checker.py      # 程式碼風格規則
│   ├── security.py           # 安全偵測規則
│   ├── complexity.py         # 複雜度分析規則
│   ├── performance.py        # 效能建議規則
│   └── best_practices.py     # 最佳實踐規則
├── formatters/          # 輸出格式化器
│   ├── base.py               # 格式化器基類
│   ├── json_fmt.py           # JSON 格式
│   ├── html_fmt.py           # HTML 報告
│   └── markdown_fmt.py       # Markdown 格式
└── tui/                 # TUI 儀表板
    └── dashboard.py          # 互動式終端介面
```

### 迭代規劃

- [x] **v1.0** -- 核心功能：6 大檢查維度、30+ 規則、多格式輸出、TUI 儀表板、平行掃描
- [ ] **v1.1** -- 增量掃描：只檢查變更的檔案，支援 Git diff 整合
- [ ] **v1.2** -- 自動修復：對部分規則提供 `--fix` 自動修復功能
- [ ] **v1.3** -- 外掛系統：支援使用者自訂檢查規則
- [ ] **v2.0** -- 類型推論引擎：基於控制流分析的跨函式類型推論

---

## 📦 打包與部署指南

### 本地安裝

```bash
# 進入專案目錄
cd pyguard-cli

# 安裝到目前 Python 環境
pip install .

# 開發模式安裝（推薦貢獻者使用）
pip install -e .
```

### 建構分發包

```bash
# 安裝建構工具
pip install build

# 建構 sdist 和 wheel
python -m build

# 建構產物位於 dist/ 目錄
ls dist/
# pyguard_cli-1.0.0-py3-none-any.whl
# pyguard-cli-1.0.0.tar.gz
```

### 安裝到指定環境

```bash
# 從 wheel 安裝
pip install dist/pyguard_cli-1.0.0-py3-none-any.whl

# 從原始碼包安裝
pip install dist/pyguard-cli-1.0.0.tar.gz
```

### Docker 部署

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .
RUN pip install .

# 掃描掛載的程式碼目錄
ENTRYPOINT ["pyguard"]
CMD ["scan", "/code"]
```

```bash
# 建構映像檔
docker build -t pyguard-cli .

# 掃描本地專案
docker run --rm -v $(pwd):/code pyguard-cli scan /code --format json
```

### 離線部署

由於 PyGuard-CLI 零外部依賴，可以直接將原始碼複製到目標環境安裝：

```bash
# 在有網路的機器上
tar czf pyguard-cli.tar.gz pyguard-cli/

# 傳輸到離線環境後
tar xzf pyguard-cli.tar.gz
cd pyguard-cli
pip install . --no-index --no-deps
```

---

## 🤝 貢獻指南

我們歡迎並感謝所有形式的貢獻！無論是提交 Bug 回報、改進建議，還是直接提交程式碼。

### 如何貢獻

1. **Fork** 本儲存庫
2. 建立特性分支：`git checkout -b feature/my-new-feature`
3. 撰寫程式碼並確保通過所有測試：`python -m pytest tests/`
4. 提交變更：`git commit -m "feat: add some awesome feature"`
5. 推送分支：`git push origin feature/my-new-feature`
6. 提交 **Pull Request**

### 開發環境建置

```bash
# 克隆儲存庫
git clone https://github.com/your-username/pyguard-cli.git
cd pyguard-cli

# 開發模式安裝
pip install -e .

# 執行測試
python -m pytest tests/ -v

# 執行特定測試
python -m pytest tests/test_rules.py -v
python -m pytest tests/test_scanner.py -v
```

### 程式碼規範

- 所有程式碼檔案使用 **UTF-8** 編碼
- 遵循 **PEP 8** 編碼規範
- 所有公開函式和類別必須包含 **docstring**
- 新增規則必須附帶對應的 **單元測試**
- 提交訊息遵循 **Conventional Commits** 規範

### 提交規範

```
feat: 新增 XXX 規則
fix: 修復 XXX 規則的誤報問題
docs: 更新 README 文件
test: 新增 XXX 規則的單元測試
refactor: 重構 XXX 模組
```

---

## 📄 開源協議

本專案基於 [MIT License](LICENSE) 開源。

```
MIT License

Copyright (c) 2024 PyGuard Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

---

<p align="center">
  Made with ❤️ by <strong>PyGuard Team</strong>
</p>

---
---

<p align="center">
  <a href="#pyguard-cli">简体中文</a> | <a href="#繁體中文">繁體中文</a> | <b>English</b>
</p>

---

# PyGuard-CLI

> A lightweight, intelligent Python code quality inspection engine. Zero external dependencies, one command, full health check for your code.

<p align="center">
  <img src="https://img.shields.io/badge/🛡️-Type_Checking-blue"> <img src="https://img.shields.io/badge/🎨-Code_Style-green"> <img src="https://img.shields.io/badge/🔒-Security-red"> <img src="https://img.shields.io/badge/🧩-Complexity-yellow"> <img src="https://img.shields.io/badge/⚡-Performance-orange"> <img src="https://img.shields.io/badge/✅-Best_Practices-purple">
</p>

---

## Table of Contents

- [Introduction](#-introduction)
- [Core Features](#-core-features)
- [Quick Start](#-quick-start)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Basic Usage](#basic-usage)
- [Detailed Guide](#-detailed-guide)
  - [CLI Reference](#cli-reference)
  - [Output Formats](#output-formats)
  - [Configuration](#configuration)
  - [TUI Dashboard](#tui-dashboard)
  - [Parallel Scanning](#parallel-scanning)
  - [Using as a Python Library](#using-as-a-python-library)
  - [CI/CD Integration](#cicd-integration)
- [Rule Categories](#-rule-categories)
- [Design Philosophy & Roadmap](#-design-philosophy--roadmap)
- [Packaging & Deployment](#-packaging--deployment)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎉 Introduction

PyGuard-CLI is a **lightweight code quality inspection tool** built for Python developers. It has zero third-party dependencies, relying entirely on the Python standard library. Using AST (Abstract Syntax Tree) static analysis, it performs comprehensive, multi-dimensional quality checks on your codebase.

Whether you are an individual developer maintaining a small project or a team managing a large codebase, PyGuard-CLI seamlessly integrates into your workflow to help you:

- 🔍 **Catch potential bugs early** -- Detect type errors, security vulnerabilities, and logic issues before your code runs
- 📏 **Enforce consistent style** -- Ensure team members follow uniform coding conventions
- 📊 **Quantify code quality** -- Gain clear visibility into code health through complexity analysis and statistical reports
- 🚀 **Zero-friction adoption** -- No dependencies to install, just `pip install` and go

### Why PyGuard-CLI?

| Feature | PyGuard-CLI | Pylint | Flake8 |
|---------|-------------|--------|--------|
| External Dependencies | **Zero** | 20+ | 10+ |
| Install Size | **< 100KB** | ~10MB | ~5MB |
| TUI Dashboard | ✅ | ❌ | ❌ |
| HTML Report | ✅ | Plugin | Plugin |
| Security Scanning | ✅ Built-in | Partial | Plugin |
| Parallel Scanning | ✅ | ❌ | ❌ |

---

## ✨ Core Features

- 🛡️ **6 inspection dimensions, 30+ rules** -- Type checking, code style, security detection, complexity analysis, performance suggestions, and best practices
- 📦 **Zero external dependencies** -- Built entirely with the Python standard library (`ast`, `argparse`, `json`, `concurrent.futures`, etc.)
- 🖥️ **Interactive TUI dashboard** -- Pure terminal ANSI interface with keyboard navigation, issue browsing, statistical charts, and file heatmaps
- 📄 **Multiple output formats** -- Colorized terminal text, JSON, HTML reports, and Markdown for any scenario
- ⚡ **Parallel scanning engine** -- Multi-process parallelism via `ProcessPoolExecutor` for significantly faster scans on large projects
- 🔧 **Flexible configuration** -- JSON config files + CLI arguments, with rule-level and category-level ignore support
- 🧪 **Comprehensive test suite** -- 44 unit tests covering all inspection rules for detection accuracy
- 🎯 **Precise issue location** -- Every issue is pinpointed to file, line, and column, with actionable fix suggestions

---

## 🚀 Quick Start

### Prerequisites

- **Python** >= 3.8 (supports 3.8 / 3.9 / 3.10 / 3.11 / 3.12)
- **OS**: Windows / macOS / Linux
- **Terminal**: ANSI escape code support required for TUI mode

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/pyguard-cli.git
cd pyguard-cli

# Option 1: Install with pip (recommended)
pip install .

# Option 2: Install with setup.py
python setup.py install

# Option 3: Editable install (changes take effect immediately)
pip install -e .
```

After installation, the `pyguard` command is automatically registered in your system PATH.

Verify the installation:

```bash
pyguard --version
# Output: pyguard 1.0.0
```

### Basic Usage

```bash
# 📁 Scan all Python files in the current directory
pyguard scan .

# 📄 Check a single file
pyguard check my_script.py

# 📊 Output in JSON format (for programmatic consumption)
pyguard scan . --format json

# 🖥️ Launch the interactive TUI dashboard
pyguard scan . --tui

# 🔴 Show only error-level issues
pyguard scan . --severity error

# 🚀 Enable parallel scanning for speed
pyguard scan . --parallel

# 🙈 Ignore specific rules
pyguard scan . --ignore STYLE001 STYLE007

# 📋 Use a custom configuration file
pyguard scan . --config my_pyguard.json

# 📝 Generate an HTML report
pyguard scan . --format html > report.html

# 📑 Generate a Markdown report
pyguard scan . --format markdown > report.md
```

---

## 📖 Detailed Guide

### CLI Reference

```
pyguard [--version]
pyguard scan <path> [options]
pyguard check <file> [options]
```

#### `scan` -- Scan a Path

Recursively scans all Python files under the specified directory or file path.

```bash
pyguard scan <path> [options]
```

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--format` | `-f` | Output format: `text` / `json` / `html` / `markdown` | `text` |
| `--severity` | `-s` | Severity filter: `error` / `warning` / `info` / `all` | `all` |
| `--ignore` | `-i` | Rule IDs to ignore (supports multiple) | none |
| `--config` | `-c` | Path to configuration file | auto-detect |
| `--parallel` | `-p` | Enable parallel scanning | off |
| `--tui` | | Launch TUI dashboard mode | off |

#### `check` -- Check a Single File

Performs a detailed quality check on a single Python file.

```bash
pyguard check <file> [options]
```

Options are the same as `scan` (except `--parallel` is not supported).

### Output Formats

#### Colorized Terminal (text, default)

The default output format uses ANSI colors to highlight issues by severity:

```
[E] TYPE001  my_script.py:15:3   Function 'process_data' missing return type annotation
[W] STYLE001 my_script.py:42:1   Line too long (135 > 120)
[I] BP003    my_script.py:3:1    Import 're' is unused
```

#### JSON Format

Structured JSON output for integration with other tools:

```bash
pyguard scan . --format json
```

```json
{
  "issues": [
    {
      "file_path": "/path/to/my_script.py",
      "line_no": 15,
      "column": 3,
      "rule_id": "TYPE001",
      "severity": "error",
      "message": "Function 'process_data' missing return type annotation",
      "category": "type",
      "suggestion": "Add return type annotation, e.g.: def process_data(...) -> ReturnType:"
    }
  ],
  "summary": {
    "files_scanned": 12,
    "files_with_issues": 5,
    "total_lines": 1580,
    "total_issues": 23,
    "error_count": 3,
    "warning_count": 12,
    "info_count": 8,
    "scan_time": 0.156
  }
}
```

#### HTML Report

Generates a styled HTML report, ideal for team reviews and archiving:

```bash
pyguard scan . --format html > report.html
```

The HTML report includes summary cards, category statistics, and a detailed issue list with responsive design for viewing in any browser.

#### Markdown Format

Generates a Markdown report, suitable for embedding in documentation or pull request descriptions:

```bash
pyguard scan . --format markdown > report.md
```

### Configuration

Create a `pyguard.json` or `.pyguard.json` file in your project root. PyGuard-CLI will automatically detect and load it:

```json
{
  "max_line_length": 120,
  "max_complexity": 10,
  "max_function_length": 50,
  "max_nesting_depth": 4,
  "max_parameters": 7,
  "max_class_length": 500,
  "ignore_rules": ["STYLE001", "STYLE007"]
}
```

#### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `max_line_length` | int | `120` | Maximum characters per line |
| `max_complexity` | int | `10` | Maximum cyclomatic complexity per function |
| `max_function_length` | int | `50` | Maximum lines per function |
| `max_nesting_depth` | int | `4` | Maximum nesting depth |
| `max_parameters` | int | `7` | Maximum parameters per function |
| `max_class_length` | int | `500` | Maximum lines per class |
| `ignore_rules` | list | `[]` | List of rule IDs to ignore |

> 💡 **Tip**: The `--ignore` CLI argument is merged with `ignore_rules` from the config file (union of both).

### TUI Dashboard

Launch the interactive terminal dashboard with the `--tui` flag:

```bash
pyguard scan . --tui
```

The TUI dashboard provides three tabs:

| Tab | Description |
|-----|-------------|
| **Issue List** | Browse all detected issues with up/down navigation and detail view |
| **Statistics** | View scan summary, issue distribution chart, and category bar chart |
| **File Heatmap** | Visualize issue density per file |

**Keyboard Shortcuts:**

| Key | Action |
|-----|--------|
| `↑` / `k` | Move selection up |
| `↓` / `j` | Move selection down |
| `Tab` | Switch tab |
| `q` / `Ctrl+C` | Exit dashboard |

### Parallel Scanning

For large projects, enable parallel scanning for a significant speed boost:

```bash
pyguard scan . --parallel
```

Parallel scanning is powered by `ProcessPoolExecutor`, automatically detecting CPU cores (up to 8 workers) and distributing files across multiple processes.

> ⚠️ **Note**: Parallel mode may not provide noticeable improvement for small file counts (< 10) due to process startup overhead.

### Using as a Python Library

Beyond the CLI, PyGuard-CLI can be used directly as a Python library in your code:

```python
from pyguard.scanner import Scanner

# Initialize the scanner (optional custom config)
scanner = Scanner(config={
    "max_line_length": 100,
    "max_complexity": 8,
})

# Scan a directory
result = scanner.scan_path("./my_project")

# Inspect results
print(f"Files scanned: {result.files_scanned}")
print(f"Total issues: {len(result.issues)}")
print(f"Errors: {result.error_count}")
print(f"Warnings: {result.warning_count}")
print(f"Info: {result.info_count}")
print(f"Scan time: {result.scan_time:.3f}s")

# Iterate through issues
for issue in result.issues:
    print(f"[{issue.severity}] {issue.rule_id} "
          f"{issue.file_path}:{issue.line_no} - {issue.message}")
    if issue.suggestion:
        print(f"  Suggestion: {issue.suggestion}")

# Check a single file
single_result = scanner.check_single_file("./my_script.py")
```

### CI/CD Integration

PyGuard-CLI uses exit codes designed for CI/CD pipeline integration:

| Exit Code | Meaning |
|-----------|---------|
| `0` | Scan completed, no error-level issues found |
| `1` | Scan completed, error-level issues found |
| `2` | CLI argument error or scan failure |

#### GitHub Actions Example

```yaml
name: Code Quality Check

on: [push, pull_request]

jobs:
  pyguard:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install PyGuard-CLI
        run: pip install .
      - name: Run PyGuard Scan
        run: pyguard scan . --format json --severity error > pyguard-report.json
      - name: Check Results
        run: |
          if grep -q '"error_count": [1-9]' pyguard-report.json; then
            echo "::error::PyGuard detected errors! Check the report."
            exit 1
          fi
```

#### Git pre-commit Hook Example

```bash
# .git/hooks/pre-commit
#!/bin/bash
echo "Running PyGuard-CLI..."
pyguard scan . --severity error
if [ $? -ne 0 ]; then
    echo "❌ PyGuard detected errors. Please fix before committing."
    exit 1
fi
echo "✅ PyGuard check passed."
```

---

## 📋 Rule Categories

PyGuard-CLI includes **6 inspection dimensions with 30+ rules**, covering every aspect of code quality.

### 🛡️ Type Checking (TYPE001 - TYPE005)

| Rule ID | Description | Severity |
|---------|-------------|----------|
| TYPE001 | Function missing return type annotation | warning |
| TYPE002 | Usage of `Any` type | info |
| TYPE003 | Parameter missing type annotation | info |
| TYPE004 | `Optional` type not handled correctly | warning |
| TYPE005 | Type annotation uses string instead of direct reference | info |

### 🎨 Code Style (STYLE001 - STYLE008)

| Rule ID | Description | Severity |
|---------|-------------|----------|
| STYLE001 | Line too long | warning |
| STYLE002 | Function missing docstring | info |
| STYLE003 | Class missing docstring | info |
| STYLE004 | Naming convention violation (class/function/variable names) | warning |
| STYLE005 | Trailing whitespace | info |
| STYLE006 | Trailing blank lines | info |
| STYLE007 | Import order not standardized | info |
| STYLE008 | Multiple consecutive blank lines | info |

### 🔒 Security Detection (SEC001 - SEC005)

| Rule ID | Description | Severity |
|---------|-------------|----------|
| SEC001 | Usage of `eval()` or `exec()` | error |
| SEC002 | Hardcoded passwords/secret keys | error |
| SEC003 | SQL injection risk | error |
| SEC004 | Unsafe `pickle` usage | warning |
| SEC005 | Using `assert` for input validation | warning |

### 🧩 Complexity Analysis (CPLX001 - CPLX005)

| Rule ID | Description | Severity |
|---------|-------------|----------|
| CPLX001 | Cyclomatic complexity too high | warning |
| CPLX002 | Function too long | warning |
| CPLX003 | Nesting depth too deep | warning |
| CPLX004 | Too many parameters | info |
| CPLX005 | Class too large | info |

### ⚡ Performance Suggestions (PERF001 - PERF005)

| Rule ID | Description | Severity |
|---------|-------------|----------|
| PERF001 | String concatenation in loop | info |
| PERF002 | Unnecessary list comprehension (e.g., `any([x for x in ...])`) | info |
| PERF003 | Global variable lookup | info |
| PERF004 | Excessive string concatenation | info |
| PERF005 | Repeated calls inside loop | info |

### ✅ Best Practices (BP001 - BP005)

| Rule ID | Description | Severity |
|---------|-------------|----------|
| BP001 | Overly broad exception catching (bare `except`) | warning |
| BP002 | Mutable default arguments | warning |
| BP003 | Unused imports | info |
| BP004 | Unused variables | info |
| BP005 | Class missing `__init__` definition | info |

---

## 💡 Design Philosophy & Roadmap

### Design Principles

PyGuard-CLI is built on the philosophy of **"lightweight but not lightweight in capability"**:

1. **Zero-dependency principle** -- Only the Python standard library is used, ensuring it runs in any Python environment without version conflict risks
2. **AST-based static analysis** -- Built on abstract syntax trees rather than regex matching, guaranteeing detection accuracy and reliability
3. **Progressive adoption** -- Works out of the box with no configuration needed, while offering rich options for advanced use cases
4. **Multi-scenario adaptability** -- CLI usage, Python library calls, CI/CD integration, and TUI interaction cover every workflow

### Architecture Overview

```
pyguard/
├── cli.py              # CLI entry point, argument parsing and command dispatch
├── scanner.py          # Core scanning engine, rule orchestration
├── models.py           # Data models (Issue, BaseRule)
├── utils.py            # Utility functions (colors, file discovery, config loading)
├── rules/              # Inspection rule modules
│   ├── type_checker.py       # Type checking rules
│   ├── style_checker.py      # Code style rules
│   ├── security.py           # Security detection rules
│   ├── complexity.py         # Complexity analysis rules
│   ├── performance.py        # Performance suggestion rules
│   └── best_practices.py     # Best practice rules
├── formatters/          # Output formatters
│   ├── base.py               # Formatter base class
│   ├── json_fmt.py           # JSON format
│   ├── html_fmt.py           # HTML report
│   └── markdown_fmt.py       # Markdown format
└── tui/                 # TUI dashboard
    └── dashboard.py          # Interactive terminal interface
```

### Roadmap

- [x] **v1.0** -- Core features: 6 inspection dimensions, 30+ rules, multi-format output, TUI dashboard, parallel scanning
- [ ] **v1.1** -- Incremental scanning: only check changed files with Git diff integration
- [ ] **v1.2** -- Auto-fix: provide `--fix` for automatic remediation of supported rules
- [ ] **v1.3** -- Plugin system: support user-defined custom inspection rules
- [ ] **v2.0** -- Type inference engine: cross-function type inference based on control flow analysis

---

## 📦 Packaging & Deployment

### Local Installation

```bash
# Navigate to the project directory
cd pyguard-cli

# Install into the current Python environment
pip install .

# Editable install (recommended for contributors)
pip install -e .
```

### Building Distribution Packages

```bash
# Install build tools
pip install build

# Build sdist and wheel
python -m build

# Build artifacts are in the dist/ directory
ls dist/
# pyguard_cli-1.0.0-py3-none-any.whl
# pyguard-cli-1.0.0.tar.gz
```

### Installing to a Specific Environment

```bash
# Install from wheel
pip install dist/pyguard_cli-1.0.0-py3-none-any.whl

# Install from source distribution
pip install dist/pyguard-cli-1.0.0.tar.gz
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .
RUN pip install .

# Scan mounted code directory
ENTRYPOINT ["pyguard"]
CMD ["scan", "/code"]
```

```bash
# Build the image
docker build -t pyguard-cli .

# Scan a local project
docker run --rm -v $(pwd):/code pyguard-cli scan /code --format json
```

### Offline Deployment

Since PyGuard-CLI has zero external dependencies, you can simply copy the source code to the target environment:

```bash
# On a machine with internet access
tar czf pyguard-cli.tar.gz pyguard-cli/

# After transferring to the offline environment
tar xzf pyguard-cli.tar.gz
cd pyguard-cli
pip install . --no-index --no-deps
```

---

## 🤝 Contributing

We welcome and appreciate contributions of all forms! Whether it's filing bug reports, suggesting improvements, or submitting code directly.

### How to Contribute

1. **Fork** this repository
2. Create a feature branch: `git checkout -b feature/my-new-feature`
3. Write code and make sure all tests pass: `python -m pytest tests/`
4. Commit your changes: `git commit -m "feat: add some awesome feature"`
5. Push the branch: `git push origin feature/my-new-feature`
6. Submit a **Pull Request**

### Setting Up the Development Environment

```bash
# Clone the repository
git clone https://github.com/your-username/pyguard-cli.git
cd pyguard-cli

# Editable install
pip install -e .

# Run all tests
python -m pytest tests/ -v

# Run specific tests
python -m pytest tests/test_rules.py -v
python -m pytest tests/test_scanner.py -v
```

### Code Standards

- All source files use **UTF-8** encoding
- Follow **PEP 8** coding conventions
- All public functions and classes must include **docstrings**
- New rules must include corresponding **unit tests**
- Commit messages follow the **Conventional Commits** specification

### Commit Message Convention

```
feat: add XXX rule
fix: resolve false positives in XXX rule
docs: update README documentation
test: add unit tests for XXX rule
refactor: refactor XXX module
```

---

## 📄 License

This project is released under the [MIT License](LICENSE).

```
MIT License

Copyright (c) 2024 PyGuard Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

---

<p align="center">
  Made with ❤️ by <strong>PyGuard Team</strong>
</p>
