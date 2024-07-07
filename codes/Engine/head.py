import pygame
import random
import numpy
import sys
from control_scheme_funcs import *
from classses import *

title = "alpha test 0.0.1"
clock = pygame.time.Clock()
clock.tick(60)
pygame.init()
width = 600
height = 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption(title)

testMap = pygame.image.load('C:/Users/Louie/Desktop/python/TheGame/testrec/map.png').convert_alpha()
