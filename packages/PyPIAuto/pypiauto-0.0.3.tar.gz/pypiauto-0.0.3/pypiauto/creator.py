# 开发人员： Xiaoqiang
# 微信公众号: XiaoqiangClub
# 开发时间： 2025-05-21 18:18:18
# 文件名称： creator.py
# 项目描述： 项目模板创建功能

import os
from typing import Optional
from datetime import datetime


def _write_file(filepath: str, content: str) -> None:
    """
    :param filepath: 文件路径
    :param content: 文件内容
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


def _file_header(filename: str, desc: str) -> str:
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return f"""# 开发人员： Xiaoqiang
# 微信公众号: XiaoqiangClub
# 开发时间： {now}
# 文件名称： {filename}
# 项目描述： {desc}

"""


PYPROJECT_TOML_TEMPLATE = """# pyproject.toml 示例模板
# 这是 PEP 518 推荐的现代 Python 构建配置文件
# 使用 Poetry 管理项目依赖和构建
[tool.poetry]
name = "{project_name}"  # 项目名称，需在PyPI唯一
version = "0.0.1"        # 版本号，建议语义化
description = "项目描述"
authors = ["Xiaoqiang <xiaoqiangclub@hotmail.com>"]
license = "MIT"          # 许可证类型

[tool.poetry.dependencies]
python = "^3.8"          # Python 版本要求
# 依赖示例
# requests = "^2.31.0"

[tool.poetry.dev-dependencies]
# 开发依赖示例
# pytest = "^7.0.0"

[tool.poetry.scripts]
# 命令行脚本入口示例
# yourcli = "{project_name}.main:main"

# 包含非py文件（如数据文件、静态文件等），详见官方文档
# include = ["your_package/data/*.json", "your_package/static/*"]

# exclude = ["tests/*"]

[tool.poetry.include]
# 示例：包含所有json文件
# pattern = "your_package/data/*.json"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
"""


def create_project_template(project_name: str, path: Optional[str] = None) -> None:
    """
    :param project_name: 项目名称
    :param path: 项目生成路径，默认为当前目录
    """
    if not project_name.isidentifier():
        print("项目名称必须为合法的Python标识符。")
        return
    base_path = os.path.abspath(path) if path else os.getcwd()
    project_path = os.path.join(base_path, project_name)
    if os.path.exists(project_path):
        print(f"目录 {project_path} 已存在，无法创建。")
        return

    # 创建目录结构
    os.makedirs(os.path.join(project_path, project_name))
    os.makedirs(os.path.join(project_path, 'examples'))

    # .gitignore
    _write_file(os.path.join(project_path, '.gitignore'), "*.pyc\n__pycache__/\nbuild/\ndist/\n*.egg-info/\n.env\n")

    # LICENSE
    _write_file(os.path.join(project_path, 'LICENSE'), "MIT License\n\nCopyright (c) 2025 Xiaoqiang")

    # README.md
    readme_content = f"""# {project_name}

项目说明：

## 捐赠
>更多内容请关注微信公众号：XiaoqiangClub
![支持我](https://gitee.com/xiaoqiangclub/xiaoqiangapps/raw/master/images/xiaoqiangclub_ad.png)
"""
    _write_file(os.path.join(project_path, 'README.md'), readme_content)

    # requirements.txt
    _write_file(os.path.join(project_path, 'requirements.txt'), "")

    # pyproject.toml（与 create_build_template 的 toml 模板保持一致）
    pyproject_content = PYPROJECT_TOML_TEMPLATE.format(project_name=project_name)
    _write_file(os.path.join(project_path, 'pyproject.toml'), pyproject_content)

    # main.py
    _write_file(os.path.join(project_path, 'main.py'), _file_header('main.py',
                                                                    '程序入口点') + "def main():\n    print('Hello, XiaoqiangClub!')\n\nif __name__ == '__main__':\n    main()\n")

    # 包__init__.py
    _write_file(os.path.join(project_path, project_name, '__init__.py'), _file_header('__init__.py', '包初始化文件'))

    # 包module.py
    _write_file(os.path.join(project_path, project_name, 'module.py'), _file_header('module.py',
                                                                                    '模块') + "def hello(name: str) -> None:\n    \"\"\"\n    :param name: 用户名\n    \"\"\"\n    print(f'你好, {name}!')\n")

    # examples/ex_module.py
    _write_file(os.path.join(project_path, 'examples', 'ex_module.py'), _file_header('ex_module.py',
                                                                                     '模块使用示例') + f"from {project_name}.module import hello\n\nhello('世界')\n")

    # publish_to_pypi.py
    _write_file(os.path.join(project_path, 'publish_to_pypi.py'),
                _file_header('publish_to_pypi.py',
                             '快速发布到PyPI脚本，需终端执行：pip install -i https://mirrors.aliyun.com/pypi/simple/ -U PyPIAuto 安装模块！') +
                "from autopypi import publish_to_pypi\n\nif __name__ == '__main__':\n    publish_to_pypi('.')\n"
                )

    print(f"项目模板已成功创建于：{project_path}")


def create_build_template(
        is_toml: bool = True,
        path: Optional[str] = None,
        project_name: str = "your_project"
) -> None:
    """
    生成 pyproject.toml 或 setup.py 的模板文件，带详细注释和示例内容。
    :param is_toml: True 生成 pyproject.toml，False 生成 setup.py
    :param path: 生成路径，默认为当前目录
    :param project_name: 项目名称（用于模板填充）
    """
    base_path = os.path.abspath(path) if path else os.getcwd()
    if is_toml:
        content = PYPROJECT_TOML_TEMPLATE.format(project_name=project_name)
        filename = os.path.join(base_path, "pyproject.toml")
    else:
        content = f'''# setup.py 示例模板
# 传统的 Python 打包配置文件，兼容 setuptools
from setuptools import setup, find_packages

setup(
    name="{project_name}",  # 项目名称，需在PyPI唯一
    version="0.0.1",        # 版本号，建议语义化
    description="项目描述",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your@email.com",
    url="https://github.com/yourname/{project_name}",
    license="MIT",          # 许可证类型
    packages=find_packages(),  # 自动发现所有包
    python_requires=">=3.8",
    install_requires=[
        # "requests>=2.31.0"
    ],
    extras_require={{
        "dev": [
            # "pytest>=7.0.0"
        ]
    }},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={{
        "console_scripts": [
            # "yourcli={project_name}.main:main"
        ]
    }},
    include_package_data=True,  # 启用MANIFEST.in
    package_data={{
        # "your_package": ["data/*.json", "static/*"]
    }},
    zip_safe=False,
)
'''
        filename = os.path.join(base_path, "setup.py")

    if os.path.exists(filename):
        print(f"{filename} 已存在，未覆盖。")
        return
    _write_file(filename, content)
    print(f"已生成模板文件：{filename}")
