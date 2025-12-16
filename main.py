import pygame as pg
import random
import time
import director
def main():
    dir = director.Director()
    dir.create_sceneMenu
    dir.create_sceneZero
    dir.loop()
    dir.change_scene(menu)
    menu.on_update()
    time.sleep(5)
    dir.change_scene(zero)
    zero.on_update()

if __name__ == '__main__':
    pg.init()
    main()