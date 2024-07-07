from pygame import *
import random
from const_datas import *
from control_scheme_funcs import *
from funcs import *
mainA_img = image.load("testrec/M_C4.png").convert_alpha()
mainB_img = image.load("testrec/M_C3.png").convert_alpha()
mainC_img = image.load("testrec/M_C3.png").convert_alpha()
testbk_img = image.load('testrec/map.png').convert_alpha()
white_bk=Surface((5000,5000))
white_bk.fill("white")
test_bk = Background(testbk_img, "testbk", Size(5000, 5000))
bk2=Background(white_bk,"UI_BK",Size(5000,5000))
test_world = World("test_world", test_bk)
UI_world = World("UI_world", bk2)
cameraA = Camera("camera A", Size(1280,720), Size(1280, 720), Position((0, 0)))

mainB = Character("mainB", Position((1800, 1800),test_world))
mainA = Character("mainA", Position((-100, -100), test_world))
mainA.set_image(mainA_img)
mainA.set_control_scheme(Basic_Move)
mainA.layer=1

mainB.set_image(mainB_img)
mainB.layer=2
mainA.show(CameraEnum.ALL_CAMERA)

mainB.show(CameraEnum.ALL_CAMERA)

'''
mainB = Character("mainB", mainB_img, Area((200,200), (400,400), testMap))
mainB.show()

mainC = Character("mainC", mainC_img, Area((400, 400), (600, 600), testMap))
mainC.show()
'''

cameraA.focus(mainA)
