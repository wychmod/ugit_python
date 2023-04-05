import os

from ugit_python.ugit import data


def write_tree(directory='.'):
    """
    将目录下的文件进行读取，blob文件进行hash，，tree文件进行递归调用，然后将扫描到的文件和文件夹的hash值进行汇总
    :param directory:
    :return:
    """
    entries = []
    with os.scandir(directory) as it:
        for entry in it:
            full = os.path.join(directory, entry.name)
            if is_ignored(full):
                continue

            if entry.is_file(follow_symlinks=False):
                type_ = 'blob'
                with open(full, 'rb') as f:
                    oid = data.hash_object(f.read())
            elif entry.is_dir(follow_symlinks=False):
                type_ = 'tree'
                oid = write_tree(full)
            entries.append((entry.name, oid, type_))

    tree = ''.join(f'{type_} {oid} {name}\n' for name, oid, type_ in sorted(entries))

    return data.hash_object(tree.encode(), 'tree')


def _iter_tree_entries(oid):
    """
    根据树的hash值，形成迭代器来获取当前树中的信息
    :param oid:
    :return:
    """
    if not oid:
        return
    tree: str = data.get_object(oid, 'tree')
    for entry in tree.encode().splitlines():
        type_, oid, name = entry.split(" ", 2)
        yield type_, oid, name


def get_tree(oid, base_path=""):
    """
    递归得到数据库,组织成树结构
    :param oid:
    :param base_path:
    :return:dict key: 路径 value: oid
    """
    result = {}
    for type_, oid, name in _iter_tree_entries(oid):
        assert '/' not in name
        assert name not in ('..', '.')
        path = os.path.join(base_path, name)
        if type_ == 'blob':
            result[path] = oid
        elif type_ == 'tree':
            result.update(get_tree(oid, path))
        else:
            assert False, f'Unknown tree entry {type_}'
    return result


def _empty_current_directory():
    """
    删除当前文件夹中的所有内容，为之后还原某次提交的文件做准备
    :return:
    """
    for root, dirnames, filenames in os.walk('./', topdown=False):
        for filename in filenames:
            path = os.path.relpath(os.path.join(root, filename))
            if is_ignored(path) or not os.path.isfile(path):
                continue
            os.remove(path)
        for dirname in dirnames:
            path = os.path.relpath(os.path.join(root, dirname))
            if is_ignored(path):
                continue
            try:
                os.rmdir(path)
            except(FileNotFoundError, OSError):
                """
                os.rmdir() 是 Python 中的一个函数，用于删除一个空目录。
                目录必须为空，否则将无法删除，函数将抛出 OSError 异常。
                如果要删除非空目录，可以使用 shutil.rmtree() 函数。
                """
                pass


def read_tree(tree_oid):
    """
    读取某棵树，首先清除当前文件夹，然后挨个进行写入
    :param tree_oid:
    :return:
    """
    _empty_current_directory()
    for path, oid in get_tree(tree_oid, base_path='./').items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            f.write(data.get_object(oid))


def is_ignored(path):
    """
    在进行文件夹处理的时候忽略.ugit文件夹
    :param path:
    :return:
    """
    return '.ugit' in path.split('/')


def commit(message):
    """
    组织提交文件的内部格式，如果有上一个提交，就将上一个提交的oid保存在当前提交中，然后重新设置这次提交的oid
    :param message:
    :return:
    """
    commit = f'tree {write_tree()}\n'

    HEAD = data.get_HEAD()
    if HEAD:
        commit += f'parent {HEAD}\n'

    commit += '\n'
    commit += f'{message}\n'

    oid = data.hash_object(commit.encode(), 'commit')

    data.set_HEAD(oid)

    return oid
