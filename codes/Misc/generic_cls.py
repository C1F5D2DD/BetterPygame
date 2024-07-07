def generic_cls(storage_name: str = '_generic_registry'):
    """ 类装饰器（工厂）。表示此类为‘泛类’
        即可以在其他类上使用@gen_cls.regiter(name)
        使其注册到基类的storage_name类属性当中
        同时给基类.create类方法用于生成实例（注册进来的类）
        create方法接受：1.类型 2.参数"""

    def decorator(gen_cls):
        setattr(gen_cls, storage_name, {})
        registry = gen_cls.__dict__[storage_name]

        @staticmethod
        def register(registry_name: str = None):
            """类装饰器工厂，用于将子类‘注册到基类上’"""
            def deco(cls_or_func):
                nonlocal registry_name
                if registry_name is None:
                    registry_name = cls_or_func.__name__
                if registry_name in registry:
                    # 命名重复
                    raise KeyError('Have had {} registered!'.format(registry_name))
                else:
                    registry[registry_name] = cls_or_func
                return cls_or_func
            return deco

        gen_cls.register = register

        @staticmethod
        def get(cls_or_func: str):
            """create方法：用来生成实例"""
            if cls_or_func in registry:
                return registry[cls_or_func]
            else:
                # 注册表中没有此类型所对应的类，则尝试用基类构造
                return gen_cls
        gen_cls.get = get
        return gen_cls
    return decorator


if __name__ == '__main__':
    @generic_cls('gens')
    class Gen:
        pass

    @Gen.register('sub1')
    class Sub1:
        def __init__(self):
            print('sub1')


    @Gen.register()
    class Sub2:
        def __init__(self, a):
            print('sub2', a)

    print(Gen.get('sub1')())
    print(Gen.get('Sub2')(213))
    print()
