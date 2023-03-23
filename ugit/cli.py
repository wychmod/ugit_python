import argparse


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

    return parser.parse_args()


def init(args):
    print('Hello, World!')
