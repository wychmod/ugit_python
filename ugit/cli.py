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

    return parser.parse_args()


def init(args):
    data.init()
    print('Initialized empty ugit repository in %s' % os.path.join(os.getcwd(), data.GIT_DIR))


def hash_object(args):
    with open(args.file, 'rb') as f:
        print(data.hash_object(f.read()))


def cat_file(args):
    # 刷新缓存区
    sys.stdout.flush()
    sys.stdout.buffer.write(data.get_object(args.object, expected=None))


def write_tree(args):
    print(base.write_tree())