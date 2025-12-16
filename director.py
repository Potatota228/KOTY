import pygame as pg
from Scenes.scene import *
from Scenes import sceneMenu
from Scenes import sceneZero
class Director():
    def __init__(self):
        LOGICAL_WIDTH = 960
        LOGICAL_HEIGHT = 540
        self.screen = pg.display.set_mode((LOGICAL_WIDTH, LOGICAL_HEIGHT))
        self.scene = None
        self.running = True
        self.clock = pg.time.Clock()
        self.FPS = 60
        # Задаем цвета
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)
        GREEN = (0, 255, 0)
        BLUE = (0, 0, 255)

        pg.init()
        pg.mixer.init()
        pg.display.set_caption("KOTY")

    def loop (self):
        while self.running:
            # Держим цикл на правильной скорости
            self.clock.tick(self.FPS)
            # Ввод процесса (события)
            for event in pg.event.get():
                # check for closing window
                if event.type == pg.QUIT:
                    quit(self)

    def change_scene(self, scene):
        self.scene = scene
        scene.on_update()

    def quit(self):
        self.running = False

    def set_screen(self, newVal):
        self.screen = newVal
    
    def create_sceneMenu(self):
        sceneMenu.SceneMenu(self)
    
    def create_sceneZero(self):
        sceneZero.SceneZero(self)