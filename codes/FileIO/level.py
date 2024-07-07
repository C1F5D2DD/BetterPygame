import json
import os

# from Engine import entities
from cmd_runner import CommandRunner


class Level:
    """
        表示一个关卡。
        属性：文件中的所有

    """
    necessary_keys = {'name', 'rec', 'bg', 'spawn_point', 'preentities', 'commands'}

    def __init__(self, path: str):
        self.path = path
        with open(path, 'rt', encoding="utf-8") as level:
            try:
                level = json.load(level)
            except json.decoder.JSONDecodeError:
                raise ValueError('Levels must come from a .json file')
            else:
                # 检查是否有的键
                lost_keys = {key for key in self.necessary_keys if key not in level}
                if lost_keys:
                    msg = 'Level object needs such attribute(s):{lost-keys}'
                else:
                    msg = ''
                if msg:
                    raise ValueError(msg.format(lost_keys=lost_keys))
                else:
                    # 该有全有
                    self.__dict__.update(level)
                    self._moblist = set()
                    # self.create_preentities()
                    self._cmd_runner = CommandRunner(self.commands)

    def tofile(self, path):
        """以json形式写入文件"""
        saving_dict = {key: getattr(self, key) for key in self.__dict__.keys() if not key.startswith('_')}
        with open(path, 'wt', encoding='utf-8') as level:
            json.dump(saving_dict, level, indent=4)

    def __repr__(self):
        return f'Level:{self.name}\n\tpath:{self.path}'


"""
    def create_preentities(self):
        生成预生成实体，写入self._moblist
        self._moblist.update(entities.Entity.get(preentity[0])(*preentity[1:])
                             for preentity in self.preentities)
"""


if __name__ == '__main__':
    # 获取路径
    path_root = os.getcwd()
    path_now = path_root
    # 获取文件路径
    for i in range(2):
        path_now, _ = os.path.split(path_now)
    # 实例化
    level_test = Level(path_now + '/recs/level/level_test.json')
    # __repr__
    print(level_test)
    # 测试写入文件
    level_test.tofile(path_now + '/recs/level/level_write_test.json')
