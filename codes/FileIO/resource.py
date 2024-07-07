# from functools import singledispatchmethod
from abc import ABC, abstractmethod

from Misc.generic_cls import generic_cls


@generic_cls('recs')
class Resource(ABC):
    """
    (抽象基类)表示一个资源
    Resource(path)->Resource实例
    属性：rec->资源本身(已加载)
        path->路径
        __loaded->已加载资源
    """

    __loaded = {}

    def __new__(cls, path):
        if path in cls.__loaded:
            # 已加载资源
            return cls.__loaded[path]
        else:
            # 未加载资源
            resource = super().__new__(cls)
            return resource

    def __init__(self, path):
        self.path = path
        self.rec = self.load(path)
        Resource.__loaded[path] = self

    # @singledispatchmethod
    @staticmethod
    @abstractmethod
    def load(path: str):
        """
        加载资源，分不同的类型
        """


if __name__ == '__main__':
    pass
