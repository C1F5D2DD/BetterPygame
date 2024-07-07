from math import hypot

from command import Command


class CommandRunner:
    """
        用于实例化后成为命令执行的上下文
        存储该关所有命令，同时便于运行命令
        签名：CommandRunner（cmds: dict, **kwargs_init）
        方法：var_dealing：处理变量名
             run_str：处理并运行一个命令
             run：运行一种命令
             kwargs：获取kwargs
    """

    def __init__(self, cmds: dict, **kwargs_init):
        # 初始化命令
        self.setup = cmds.get('setup', '').split('\n')
        # 循环命令
        self.loop = cmds.get('loop', '').split('\n')
        # 定位命令
        self.positional = {pos: cmds for pos, cmds in cmds.items() if isinstance(pos, tuple)}
        # 变量存储
        self.cmd_vars = {}
        # 初始化时我能获取到的关键字
        self.kwargs_init = kwargs_init
        self.player = kwargs_init.get('player', None)

    @staticmethod
    def var_dealing(cmds: str, **kwargs):
        """
            静态方法，用来处理变量
            传入一个命令字符串，以及一个包含vars等键的kwargs字典
            返回一个列表，[0]为命令头，[1:]为修改后参数
        """
        # print(cmds)
        cmd = cmds.split()
        cmd_adjusted = []
        for part in cmd:
            if part in Command.cmds:
                # 命令头
                part_adjusted = part
            elif part in kwargs:
                # 特殊变量名，如player
                # 可能应对vars进行特殊处理（也在kwargs中）
                part_adjusted = kwargs[part]
            elif part in kwargs['cmd_vars']:
                # 变量名
                part_adjusted = kwargs['cmd_vars'][part]
            else:
                # 常量，不做处理
                part_adjusted = part
            cmd_adjusted.append(part_adjusted)
        return cmd_adjusted

    @property
    def kwargs(self):
        """
            用来获取自己的kwargs
        """
        kwargs = {'cmd_vars': self.cmd_vars, 'player': self.player}
        kwargs.update(self.kwargs_init)
        return kwargs

    @staticmethod
    def run_str(cmds: str, **kwargs):
        """
            处理并运行命令字符串
            命令应无返回值，除了setup
        """
        cmd_list = CommandRunner.var_dealing(cmds, **kwargs)
        # print(cmd_list[0])
        return Command.get(cmd_list[0])(*cmd_list[1:], **kwargs)

    def run(self, cmd_type: str | tuple):
        match cmd_type:
            case 'setup':
                for cmd in self.setup:
                    self.run_str(cmd, **self.kwargs)
            case 'loop':
                for cmd in self.loop:
                    # print(cmd)
                    self.run_str(cmd, **self.kwargs)
            case (int() as x, int() as y):
                for pos, cmds in self.positional.items():
                    cmds = cmds.split('\n')
                    # setup命令（返回字典），获取半径
                    setup = self.run_str(cmds[0], **self.kwargs)
                    radius = setup['radius']
                    # print(hypot(x - pos[0], y - pos[1]), radius)
                    if hypot(x - pos[0], y - pos[1]) <= radius:
                        for cmd in cmds[1:]:
                            self.run_str(cmd, **self.kwargs)
            case _:
                raise ValueError(f'Can\'t run {cmd_type} cmds')

    def __repr__(self):
        return f'CommandRunner(setup = {self.setup}\
                 \n\tloop = {self.loop}\
                 \n\tpositional = {self.positional})'


if __name__ == '__main__':
    # 测试用命令
    main_cmds = {'setup': 'var aa 123\n'
                          'print 412\n'
                          'print aa\n'
                          'print cmd_vars\n'
                          'print test',
                 'loop': 'print aa\n'
                         'print loop',
                 (0, 0): 'setup 2\n'
                         'var bb 00\n'
                         'print 0,0',
                 (5, 5): 'setup 1\n'
                         'print 5,5'}
    # kwargs_init
    main_kwargs = {'test': 666, 'player': None}
    # 实例化
    cmd_runner = CommandRunner(main_cmds, **main_kwargs)
    # __repr__
    print(cmd_runner)
    # 测试setup
    print('*' * 10 + ' setup testing ' + '*' * 10)
    cmd_runner.run('setup')
    # 测试loop
    print('*' * 10 + ' loop testing ' + '*' * 10)
    cmd_runner.run('loop')
    # 测试两个定位
    print('*' * 10 + ' positional(1, 0) testing ' + '*' * 10)
    cmd_runner.run((1, 0))

    CommandRunner.run_str('print bb', **cmd_runner.kwargs)
    print('*' * 10 + ' positional(4, 5) testing ' + '*' * 10)
    cmd_runner.run((4, 5))
