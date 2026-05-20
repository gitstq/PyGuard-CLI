"""
PyGuard-CLI 安装配置

使用 setuptools 进行包安装配置。
"""

from setuptools import setup, find_packages

setup(
    name="pyguard-cli",
    version="1.0.0",
    description="轻量级Python代码质量智能巡检引擎",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="PyGuard Team",
    license="MIT",
    python_requires=">=3.8",
    packages=find_packages(),
    package_dir={"": "."},
    entry_points={
        "console_scripts": [
            "pyguard=pyguard.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Quality Assurance",
    ],
)
