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
    _write_file(os.path.join(project_path, 'README.md'), f"# {project_name}\n\n项目说明：\n")

    # requirements.txt
    _write_file(os.path.join(project_path, 'requirements.txt'), "")

    # pyproject.toml
    pyproject_content = f"""[tool.poetry]
name = "{project_name}"
version = "0.0.1"
description = ""
authors = ["Xiaoqiang <xiaoqiangclub@hotmail.com>"]

[tool.poetry.dependencies]
python = "^3.8"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
"""
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
                _file_header('publish_to_pypi.py', '快速发布到PyPI脚本') +
                "from autopypi import publish_to_pypi\n\nif __name__ == '__main__':\n    publish_to_pypi('.')\n"
                )

    print(f"项目模板已成功创建于：{project_path}")
