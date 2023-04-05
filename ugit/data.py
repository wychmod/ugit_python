import hashlib
import os

GIT_DIR = '.ugit'
GIT_OBJECT_DIR = os.path.join(GIT_DIR, "objects")


def init():
    """
    创建.git文件夹及子目录
    :return:
    """
    os.makedirs(GIT_DIR)
    os.makedirs(GIT_OBJECT_DIR)


def set_HEAD(oid):
    """
    在HEAD文件中将当前commit的内容和信息的hash值进行保存
    :param oid:
    :return:
    """
    with open(os.path.join(GIT_DIR, 'HEAD'), 'w') as f:
        f.write(oid)


def get_HEAD():
    """
    读取HEAD文件
    :return:
    """
    if os.path.isfile(os.path.join(GIT_DIR, 'HEAD')):
        with open(os.path.join(GIT_DIR, 'HEAD')) as f:
            return f.read().strip()


def hash_object(data, type_='blob'):
    """
    创建对象文件，写入文件，并将文件hash，返回hash值
    :param data: 文件数据
    :return: oid值
    """
    obj = type_.encode() + b'\x00' + data
    oid = hashlib.sha1(obj).hexdigest()
    with open(os.path.join(GIT_OBJECT_DIR, oid), 'wb') as out:
        out.write(obj)
    return oid


def get_object(oid, expected='blob'):
    """
    根据oid，type进行读取文件，并且判断type是否一致
    :param oid:
    :param expected:
    :return:
    """
    with open(os.path.join(GIT_OBJECT_DIR, oid), 'rb') as f:
        obj = f.read()

    type_, _, content = obj.partition(b'\x00')
    type_ = type_.decode()

    if expected is not None:
        assert type_ == expected, f'Expected {expected}, got {type_}'
    return content
