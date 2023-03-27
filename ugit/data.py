import hashlib
import os

GIT_DIR = '.ugit'
GIT_OBJECT_DIR = os.path.join(GIT_DIR, "objects")


def init():
    os.makedirs(GIT_DIR)
    os.makedirs(GIT_OBJECT_DIR)


def hash_object(data):
    """
    创建对象文件，写入文件
    :param data: 文件数据
    :return: oid值
    """
    oid = hashlib.sha1(data).hexdigest()
    with open(os.path.join(GIT_OBJECT_DIR, oid), 'wb') as out:
        out.write(data)
    return oid
