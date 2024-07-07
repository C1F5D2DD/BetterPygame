import sys
import time

from testhead import *
import pygame
import control_scheme_funcs
import pygame_init

nowfps = 0
ft = font.SysFont('arial', 40)
txt = ft.render(str(nowfps), True, (0, 0, 255), (0, 0, 0))
fps_shower = Character('fps_shower', Position((2300, 2300), UI_world))
fps_shower.set_image(txt)
cameraB = Camera("cameraFPS", Size(200, 100), Size(200, 100), Position((0, 0)))
fps_shower.show(cameraB)

cameraB.focus(fps_shower)


def main_loop():
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        for character in character_list.values():
            character.control_scheme.run()
            character.show()
            character.renew()

        for camera in camera_list.values():
            if camera.target != none:
                camera.shoot()
                camera.refocus()
        clock.tick(999)
        if clock.get_fps() != 0:
            pygame_init.delta = 1 / clock.get_fps()
        else:
            pygame_init.delta = 0
        nowfps = int(clock.get_fps())
        txt = ft.render('FPS' + str(nowfps), True, (0, 0, 255), (0, 0, 0))
        fps_shower.protected_img_list = txt
        pygame.display.flip()
        screen.fill('white')
        # screen.fill("black")


main_loop()