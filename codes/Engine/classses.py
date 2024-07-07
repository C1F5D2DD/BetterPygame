from math import *
from pygame_init import *
from const_datas import *
from math import *
from funcs import *


class control_scheme:
    def __init__(self, function):
        self.target = None
        self.function = function
        self.iter_func = None

    def run(self):
        if not (self.iter_func is None):
            next(self.iter_func)

    def set_target(self, target):
        self.target = target
        self.iter_func = self.function(target)

    def copy(self):
        return control_scheme(self.function)


def _none_scheme(target):
    return


None_scheme = control_scheme(_none_scheme)


class Position:
    def __init__(self, point, world=none):
        self.X = point[0]
        self.Y = point[1]
        self.world = world

    def __str__(self):
        return '(' + str(self.X) + ',' + str(self.Y) + ')'

    def __repr__(self):
        return str(self) + ' at ' + str(self.world)


class Size:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def __str__(self):
        return '(' + str(self.width) + ',' + str(self.height) + ')'

    def __repr__(self):
        return str(self)

    def __mul__(self, other):
        new_width = self.width * other
        new_height = self.height * other
        return Size(new_width, new_height)

    def __rmul__(self, other):
        new_width = self.width * other
        new_height = self.height * other
        return Size(new_width, new_height)

    def __imul__(self, other):
        self.width *= other
        self.height *= other
        return self


bk_list = {}


class Background:
    def __init__(self, img: Surface, bk_name, size: Size):
        self.image = img
        self.name = bk_name
        self.size = size
        bk_list[self.name] = self

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


world_list = {}


class World:
    def __init__(self, name, background: Background):
        self.name = name
        self.background = background
        world_list[self.name] = self
        self.area = Area((0, 0), (self.background.size.width, self.background.size.height), self)
        self.waiting_list = {}
        self.layer_num = []

    def __str__(self):
        return str(self.name)


class Area:
    def __init__(self, pos1: tuple, pos2: tuple, world: World):
        self.point1 = Position(pos1, world)
        self.point2 = Position(pos2, world)
        self.size = Size(abs(self.point1.X - self.point2.X), abs(self.point1.Y - self.point2.Y))
        self.position = Position((min(self.point1.X, self.point2.X), min(self.point1.Y, self.point2.Y)), world)
        self.top = self.position.Y
        self.left = self.position.X
        self.bottom = self.position.Y + self.size.height
        self.right = self.position.X + self.size.height
        self.world = world

    def __repr__(self):
        return 'an area at world: ' + str(self.map) + '+pos1: ' \
            + str(self.point1) + 'pos2: ' + str(self.point2)

    def __getattr__(self, item):
        match item:
            case 'x':
                return self.left
            case 'y':
                return self.top
            case 'X':
                return self.left
            case 'Y':
                return self.top
            case "left_top":
                return self.left, self.top
            case "right_bottom":
                return self.right, self.bottom

    def setPosition(self, x, y, new_world=none):
        self.top = y
        self.left = x
        self.bottom = self.top + self.size.height
        self.right = self.left + self.size.width
        if new_world != none:
            self.point1 = Position((x, y), new_world)
            self.point2 = Position((self.right, self.bottom), new_world)
            self.world = new_world
        else:
            self.point1 = Position((x, y), self.world)
            self.point2 = Position((self.right, self.bottom), self.world)

    def inside(self, target):
        if self.top < target.top:
            return False
        if self.left < target.left:
            return False
        if self.bottom > target.bottom:
            return False
        if self.right > target.right:
            return False
        return True

    def has_Overlapped(self, target):
        if self.world != target.world:
            return False
        if self.bottom < target.top:
            return False
        if self.top > target.bottom:
            return False
        if self.left > target.right:
            return False
        if self.right < target.left:
            return False
        return True

    def getOverlap(self, target):
        if self.has_Overlapped(target) == false:
            return none

        ol_top = 0
        ol_bottom = 0

        ol_left = 0
        ol_right = 0
        if target.top <= self.top <= target.bottom <= self.bottom:
            ol_top = self.top
            ol_bottom = target.bottom
        if self.top <= target.top <= self.bottom <= target.bottom:
            ol_top = target.top
            ol_bottom = self.bottom
        if target.top <= self.top <= self.bottom <= target.bottom:
            ol_top = self.top
            ol_bottom = self.bottom
        if self.top <= target.top <= target.bottom <= self.bottom:
            ol_top = target.top
            ol_bottom = target.bottom
        if self.left <= target.left <= self.right <= target.right:
            ol_left = target.left
            ol_right = self.right
        if target.left <= self.left <= target.right <= self.right:
            ol_left = self.left
            ol_right = target.right
        if target.left <= self.left <= self.right <= target.right:
            ol_left = self.left
            ol_right = self.right
        if self.left <= target.left <= target.right <= self.right:
            ol_left = target.left
            ol_right = target.right
        ol_area = Area((ol_left, ol_top), (ol_right, ol_bottom), self.world)
        return ol_area

    def move(self, length, angle_deg):
        self.setPosition(self.x, self.y - length * sin(radians(angle_deg)))
        self.setPosition(self.x + length * cos(radians(angle_deg)), self.y)

    def map_coordinate_to(self, target):
        if self.world != target.world:
            raise ValueError("two area at different world!")
        else:
            _x = self.x - target.x
            _y = self.y - target.y
            pos1 = (_x, _y)
            pos2 = (_x + self.size.width, _y + self.size.height)
            return Area(pos1, pos2, None)


camera_list = {}


class Camera:
    def __init__(self, camera_name, observe_size: Size | tuple, screen_size: Size | tuple,
                 screen_position: Position | tuple, never_work=False):
        self.world = None
        if type(screen_size) is tuple:
            screen_size = Size(screen_size[0], screen_size[1])
        self.screen_size = screen_size
        if type(screen_position) is tuple:
            screen_position = Position((screen_position[0], screen_position[1]))
        self.screen_position = screen_position
        if type(observe_size) is tuple:
            observe_size = Size(observe_size[0], observe_size[1])
        self.observe_size = observe_size
        self.target = None
        self.observe_position = None
        self.observe_area = None
        self.name = camera_name
        if not never_work:
            camera_list[self.name] = self
            self.k_width = screen_size.width / observe_size.width
            self.k_height = screen_size.height / observe_size.height
        self.tmp_screen = Surface((self.observe_size.width, self.observe_size.height)).convert_alpha()
        self.tag_list = {}

    def __getattr__(self, item):
        return self.tag_list[item]

    def __repr__(self):
        return 'the camera:' + self.name + ' looking at ' + str(self.target.area.world)

    def focus(self, target):
        self.target = target
        _map = target.area.map
        x = target.area.x + target.area.size.width / 2 - self.observe_size.width / 2
        y = target.area.y + target.area.size.height / 2 - self.observe_size.height / 2
        self.observe_position = Position((x, y), _map)
        self.observe_area = Area((self.observe_position.X, self.observe_position.Y),
                                 (self.observe_position.X + self.observe_size.width,
                                  self.observe_position.Y + self.observe_size.height),
                                 self.target.world)
        self.world = self.target.world

    def refocus(self):
        _world = self.target.area.world
        x = self.target.area.position.X + self.target.area.size.width / 2 - self.observe_size.width / 2
        y = self.target.area.position.Y + self.target.area.size.height / 2 - self.observe_size.height / 2
        self.observe_position = Position((x, y), _world)
        self.observe_area.setPosition(x, y)
        self.world = self.target.world

    def show_at(self, x, y):
        self.screen_position = Position((x, y))

    def shoot(self):
        # 判断是否需要拉伸
        # no
        if self.k_width == 1.0 and self.k_height == 1.0:
            first_out = screen
        # yes
        else:
            first_out = Surface((self.observe_size.width, self.observe_size.height))
        # process background
        tmp_left = self.observe_area.left
        tmp_top = self.observe_area.top
        tmp_right = self.observe_area.right
        tmp_bottom = self.observe_area.bottom
        if tmp_right < 0 or tmp_bottom < 0:
            raise ValueError(str(self) + " is completely off the map")
        if tmp_left < 0:
            tmp_left = 0
        if tmp_top < 0:
            tmp_top = 0
        if tmp_right > self.world.area.right:
            tmp_right = self.world.area.right
        if tmp_bottom > self.world.area.bottom:
            tmp_bottom = self.world.area.bottom
        tmp_bk = self.world.background.image.subsurface(tmp_left, tmp_top, tmp_right - tmp_left, tmp_bottom - tmp_top)
        first_out.blit(tmp_bk, (tmp_left - self.observe_area.left + self.screen_position.X,
                                tmp_top - self.observe_area.top + self.screen_position.Y))
        # process characters
        _layer_num = self.world.layer_num.copy()
        _layer_num = sorted(_layer_num, reverse=True)
        for layer in _layer_num:
            for items in self.world.waiting_list[layer].values():
                if not (self in items.camera_list.values()):
                    print("passed"+str(items)+str(self))
                    continue
                if items.area.inside(self.observe_area):
                    try:
                        _x = items.position.X - self.observe_position.X + self.screen_position.X
                        _y = items.position.Y - self.observe_position.Y + self.screen_position.Y
                        first_out.blit(items.image, (_x, _y))
                    except AttributeError:
                        print(items, "error at shot")
                    continue
                if items.area.has_Overlapped(self.observe_area):
                    __area = items.area.getOverlap(self.observe_area)
                    _area = __area.map_coordinate_to(items.area)
                    l = _area.left
                    t = _area.top
                    r = _area.right
                    b = _area.bottom
                    h = _area.size.height
                    w = _area.size.width
                    if w < 0:
                        w = 0
                    if h < 0:
                        h = 0
                    if t < 0:
                        t = 0
                    if l < 0:
                        l = 0
                    # if not (l < 0 or t < 0 or _area.width > items.area.width or _area.height > items.area.height):
                    try:
                        tmp_img = items.image.subsurface(l, t, w, h)
                        _x = items.position.X + l - self.observe_position.X + self.screen_position.X
                        _y = items.position.Y + t - self.observe_position.Y + self.screen_position.Y
                        first_out.blit(tmp_img, (_x, _y))
                    except ValueError:
                        print(items.area.width, items.area.height, l, t, w, h, r, b, "!", items, self)
        # final process
        if not (first_out is screen):
            out = transform.smoothscale(first_out, (self.screen_size.width, self.screen_size.height))
            screen.blit(out, (self.screen_position.X, self.screen_position.Y))
        return


character_list = {}


class Character:
    def __init__(self, name, position: Position):
        self.name = name
        self.area = None
        self.world = position.world
        self.init_position = position
        self.protected_img_list = None
        self.image = None
        self.tag_list = {}
        self.control_scheme = None_scheme
        self.layer = 1
        self.camera_list = {}
        character_list[self.name] = self

    def __getattr__(self, item):
        if item in self.tag_list.keys():
            return self.tag_list[item]
        else:
            match item:
                case 'position':
                    return Position((self.area.x, self.area.y), self.world)

    def __repr__(self):
        return self.name + ' at ' + self.world.name

    def set_control_scheme(self, schem):
        self.control_scheme = schem.copy()
        self.control_scheme.set_target(self)

    def set_image(self, img: Surface):
        try:
            self.protected_img_list = img
            w = img.get_rect().width
            h = img.get_rect().height
            x = self.init_position.X
            y = self.init_position.Y
            self.area = Area((x, y), (x + w, y + h), self.world)
            self.image = img.copy()
        except AttributeError:
            print(self, 'error at set')

    def renew_image(self):
        img = self.protected_img_list
        w = img.get_rect().width
        h = img.get_rect().height
        x = self.position.X
        y = self.position.Y
        self.area = Area((x, y), (x + w, y + h), self.world)
        self.image = img.copy()

    def renew_world(self):
        self.world = self.area.world

    def reset_world(self, new_world: World):
        self.area.world = new_world
        self.renew_world()

    def renew(self):
        self.renew_world()
        self.renew_image()

    def show(self, cam=CameraEnum.DEFAULT_CAMERA):
        if cam is CameraEnum.ALL_CAMERA:
            self.camera_list = camera_list.copy()
            if self.layer not in self.world.waiting_list.keys():
                self.world.waiting_list[self.layer]={}
            self.world.waiting_list[self.layer][self.name] = self
            if self.layer not in self.world.layer_num:
                self.world.layer_num.append(self.layer)
        if cam is CameraEnum.DEFAULT_CAMERA:
            if self.layer not in self.world.waiting_list.keys():
                self.world.waiting_list[self.layer]={}
            self.world.waiting_list[self.layer][self.name] = self
            if self.layer not in self.world.layer_num:
                self.world.layer_num.append(self.layer)
        if cam is CameraEnum.NULL_CAMERA:
            self.camera_list.clear()
        if type(cam) is Camera:
            self.camera_list = {cam.name:cam}
            if self.layer not in self.world.waiting_list.keys():
                self.world.waiting_list[self.layer]={}
            self.world.waiting_list[self.layer][self.name] = self
            if self.layer not in self.world.layer_num:
                self.world.layer_num.append(self.layer)
