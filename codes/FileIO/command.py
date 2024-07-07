from Misc.generic_cls import generic_cls


@generic_cls('cmds')
class Command:
    """
    接口
    用于表示一串命令（游戏内部）
    参数：commands:str
    方法：__call__
    """


"""
    命令定义：
    @Command.register(~~~~)
    def ~~~~(*args,**kwargs):
        ~~~~~~~~
    在命令内部，最好先进行参数静态检查
"""


@Command.register('print')
def test_print(*args, **kwargs):
    """
        测试用命令
    """
    print(f'print{args}')


@Command.register()
def setup(*args, **kwargs):
    """
        初始化命令，必须放在定位命令的第一句
    """
    if len(args) != 1:
        raise TypeError(f'setup takes exactly one argument ({len(args)} given)')
    setup_dict = {'radius': int(args[0])}
    return setup_dict


@Command.register()
def var(*args, **kwargs):
    """
        设置变量，初始值可选（未提供则为None）
    """
    args_num = len(args)
    if args_num != 1 and args_num != 2:
        raise TypeError(f'var takes exactly one or two argument ({args_num} given)')
    else:
        var_name = args[0]
        try:
            initial = args[1]
        except IndexError:
            initial = None
        var_dict = kwargs['cmd_vars']
        if var_name in var_dict:
            raise KeyError(f'Have had {var_name} var!')
        else:
            var_dict[var_name] = initial

# print(Command.cmds)
