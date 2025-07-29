# 导入必要的模块
# setuptools 是 Python 中用于打包和分发的增强工具，setup 是核心函数，用于定义包的元数据和配置；
# find_packages 用于自动发现项目中的包（即包含 __init__.py 的目录）。
from setuptools import setup, find_packages

setup(
    name="todo_cli_kyra_pure_python",          # 项目名称
    version="0.1",            # 版本号（必填，遵循语义化版本规范）
    author="kyra",                # 作者
    author_email="m13409971925@163.com",  # 作者邮箱
    description="A command line todo tool",  # 项目简介
    url="https://gitee.com/a1_dong-ry/todo_cli",  # 项目主页 URL
    classifiers=[                      # 项目分类器（必填，用于 PyPI 分类检索）
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(where="src"),  # 在src目录下查找包,自动发现所有包（需项目结构规范）
    package_dir={"": "src"},  # 告诉setuptools包在src目录下
    include_package_data=True,         # 是否包含包内非代码文件（需配合 MANIFEST.in）
    # 依赖管理
    install_requires=[ # 必须安装的
        "click>=8.1.3",  # 命令行接口
        "fuzzywuzzy>=0.18.0",  # 模糊搜索
        "jieba>=0.42.1",  # 中文分词
        "tabulate>=0.9.0",  # 表格输出
        "python-dateutil>=2.8.2",  # 日期解析
        "dataclasses>=0.8; python_version < '3.7'",  # 兼容 Python 3.6
    ],
    extras_require={  # 可选安装的
        "visualization": [  # 数据可视化功能（可选）
            "matplotlib>=3.7.1",
            "wordcloud>=1.8.2.2",
        ],
        "notification": [  # 系统通知功能（可选）
            "plyer>=2.0.0",
        ],
        "dev": [  # 开发环境
            "pytest>=7.3.1",
            "flake8>=6.0.0",
            "black>=23.3.0",
            "isort>=5.12.0",
        ],
        "docs": [  # 文档生成
            "sphinx>=6.2.1",
            "sphinx-rtd-theme>=1.2.0",
        ],
    },

    entry_points={            # 命令行入口
        "console_scripts": [
            "todo-cli=todo_cli.main:main"
        ]
    },
    python_requires=">=3.6",           # 支持的 Python 版本范围
)