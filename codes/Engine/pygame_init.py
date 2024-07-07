from pygame import *

init()
# flags = FULLSCREEN | DOUBLEBUF
title = "alpha test 0.0.2"
clock = time.Clock()
delta=0
screen_width = 1280
screen_height = 720
screen = display.set_mode((screen_width, screen_height))
display.set_caption(title)
ft = font.SysFont('arial', 40)
show_pos = {}
# pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
