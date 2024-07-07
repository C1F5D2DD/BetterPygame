import time

from classses import *
import pygame_init


def _basic_move(target):
    i = 0
    T = 0.005
    while 1:
        i *= -1
        pressed = key.get_pressed()
        # print(pressed)
        if pressed[K_w]:
            target.area.move((4 + i) * pygame_init.delta / T, 90)
        # print("w")
        if pressed[K_s]:
            target.area.move((4 + i) * pygame_init.delta / T, -90)
            # print("s")
        if pressed[K_a]:
            target.area.move((4 + i) * pygame_init.delta / T, 180)
            # print("a")
        if pressed[K_d]:
            target.area.move((4 + i) * pygame_init.delta / T, 0)
        #print(pygame_init.delta)
        yield None


Basic_Move = control_scheme(_basic_move)
