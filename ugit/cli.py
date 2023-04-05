import argparse
import os
import sys

from . import data
from . import base


def main():
    # 实例化parse对象，里面有读取命令行的对象映射
    args = parse_args()
    args.func(args)


def parse_args():
    """
    命令行指令解析函数
    :return:
    """
    parser = argparse.ArgumentParser()

    commands = parser.add_subparsers(dest='command')
    commands.required = True

    init_parser = commands.add_parser('init')
    init_parser.set_defaults(func=init)

    hash_object_parser = commands.add_parser('hash-object')
    hash_object_parser.set_defaults(func=hash_object)
    hash_object_parser.add_argument('file')

    cat_file_parser = commands.add_parser('cat-file')
    cat_file_parser.set_defaults(func=cat_file)
    cat_file_parser.add_argument('object')

    write_tree_parser = commands.add_parser('write-tree')
    write_tree_parser.set_defaults(func=write_tree)

    read_tree_parser = commands.add_parser('read-tree')
    read_tree_parser.set_defaults(func=read_tree)
    read_tree_parser.add_argument('tree')

    commit_parser = commands.add_parser('commit')
    commit_parser.set_defaults(func=commit)
    commit_parser.add_argument('-m', '--message', required=True)

    return parser.parse_args()


def init(args):
    """
    初始化git环境
    :param args:
    :return:
    """
    data.init()
    print('Initialized empty ugit repository in %s' % os.path.join(os.getcwd(), data.GIT_DIR))


def hash_object(args):
    """
    将读取到的文件传给data.hash_object进行hash保存
    :param args:
    :return:
    """
    with open(args.file, 'rb') as f:
        print(data.hash_object(f.read()))


def cat_file(args):
    """
    刷新缓存区，输出读取的文件到命令行
    :param args:
    :return:
    """
    sys.stdout.flush()
    sys.stdout.buffer.write(data.get_object(args.object, expected=None))


def write_tree(args):
    """
    将当前的目录进行存储
    :param args:
    :return:
    """
    print(base.write_tree())


def read_tree(args):
    """
    根据hash值对树结构的文件夹进行读取
    :param args:
    :return:
    """
    print(base.read_tree(args.tree))


def commit(args):
    """
    运用提交的方式保存当前的目录结构
    :param args:
    :return:
    """
    print(base.commit(args.message))
