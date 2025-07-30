# 开发人员： Xiaoqiang
# 微信公众号: XiaoqiangClub
# 开发时间： 2025-05-21 18:18:18
# 文件名称： publisher.py
# 项目描述： 发布到PyPI功能

import os
import subprocess
import shutil
from typing import Optional


def publish_to_pypi(
        pypi_token: str,
        path: Optional[str] = None,
        cleanup: bool = False
) -> None:
    """
    :param pypi_token: PyPI Token
    :param path: 项目目录，默认为当前目录
    :param cleanup: 是否在发布后删除dist和构建目录，默认False
    """
    project_path = os.path.abspath(path) if path else os.getcwd()
    os.chdir(project_path)
    dist_path = os.path.join(project_path, "dist")
    build_path = os.path.join(project_path, "build")
    egg_info_path = None
    # 查找egg-info目录
    for item in os.listdir(project_path):
        if item.endswith('.egg-info'):
            egg_info_path = os.path.join(project_path, item)
            break

    if os.path.exists('pyproject.toml'):
        print("检测到 pyproject.toml，使用 Poetry 方式发布。")
        try:
            subprocess.run(['poetry', 'build'], check=True)
            # 使用token发布
            env = os.environ.copy()
            env['POETRY_PYPI_TOKEN_PYPI'] = pypi_token
            subprocess.run(['poetry', 'publish', '--username', '__token__', '--password', pypi_token], check=True,
                           env=env)
            print("发布成功！")
        except Exception as e:
            print(f"发布失败：{e}")
    elif os.path.exists('setup.py'):
        print("检测到 setup.py，使用 setuptools 方式发布。")
        try:
            subprocess.run(['python', 'setup.py', 'sdist', 'bdist_wheel'], check=True)
            upload_cmd = ['twine', 'upload', 'dist/*']
            env = os.environ.copy()
            env['TWINE_USERNAME'] = '__token__'
            env['TWINE_PASSWORD'] = pypi_token
            subprocess.run(upload_cmd, check=True, env=env)
            print("发布成功！")
        except Exception as e:
            print(f"发布失败：{e}")
    else:
        print("未检测到 pyproject.toml 或 setup.py，无法发布。")
        return

    if cleanup:
        # 删除dist、build、egg-info目录
        if os.path.exists(dist_path):
            shutil.rmtree(dist_path)
            print("已删除dist目录。")
        if os.path.exists(build_path):
            shutil.rmtree(build_path)
            print("已删除build目录。")
        if egg_info_path and os.path.exists(egg_info_path):
            shutil.rmtree(egg_info_path)
            print("已删除egg-info目录。")
