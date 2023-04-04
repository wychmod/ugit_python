import hashlib
import os

GIT_DIR = '.ugit'
GIT_OBJECT_DIR = os.path.join(GIT_DIR, "objects")


def init():
    os.makedirs(GIT_DIR)
    os.makedirs(GIT_OBJECT_DIR)


def set_HEAD(oid):
    with open(os.path.join(GIT_DIR, 'HEAD'), 'w') as f:
        f.write(oid)


def hash_object(data, type_='blob'):
    """
    创建对象文件，写入文件
    :param data: 文件数据
    :return: oid值
    """
    obj = type_.encode() + b'\x00' + data
    oid = hashlib.sha1(obj).hexdigest()
    with open(os.path.join(GIT_OBJECT_DIR, oid), 'wb') as out:
        out.write(obj)
    return oid


def get_object(oid, expected='blob'):
    with open(os.path.join(GIT_OBJECT_DIR, oid), 'rb') as f:
        obj = f.read()

    type_, _, content = obj.partition(b'\x00')
    type_ = type_.decode()

    if expected is not None:
        assert type_ == expected, f'Expected {expected}, got {type_}'
    return content
