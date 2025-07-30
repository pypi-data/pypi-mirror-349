# 开发人员： Xiaoqiang
# 微信公众号: XiaoqiangClub
# 开发时间： 2025-05-21 18:18:18
# 文件名称： cli.py
# 项目描述： 命令行接口

import argparse
import sys
from .creator import create_project_template
from .publisher import publish_to_pypi


def main():
    parser = argparse.ArgumentParser(
        prog='autopypi',
        description='AutoPyPI：一键创建Python项目模板并发布到PyPI。'
    )
    subparsers = parser.add_subparsers(dest='command')

    # 创建项目模板
    parser_create = subparsers.add_parser(
        'create',
        help='创建Python项目模板'
    )
    parser_create.add_argument(
        '-n', '--name', required=True, type=str, help='项目名称'
    )
    parser_create.add_argument(
        '-p', '--path', required=False, type=str, default=None, help='项目生成路径，默认为当前目录'
    )

    # 发布到PyPI
    parser_publish = subparsers.add_parser(
        'publish',
        help='将指定目录的Python模块发布到PyPI'
    )
    parser_publish.add_argument(
        '-d', '--dir', required=False, type=str, default=None, help='项目目录，默认为当前目录'
    )

    if len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1] in ['create', 'publish']):
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    if args.command == 'create':
        create_project_template(args.name, args.path)
    elif args.command == 'publish':
        publish_to_pypi(args.dir)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
