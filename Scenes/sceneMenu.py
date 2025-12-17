import pygame as pg
from .scene import Scene
from config import BLUE
class MenuScene(Scene):
    def __init__(self, director):
        super().__init__(director)
        try:
            bg_path = "./images/menu.png"
            self.bg = pg.image.load(bg_path).convert_alpha()
            self.bg_rect = self.bg.get_rect()
        except Exception as e:
            print("Не удалось загрузить фоновое изображение:", e)
            self.bg_image = None
        # try:
        #     bg_path = "./images/buttons/button.png"
        #     self.bg = pg.image.load(bg_path).convert_alpha()
        #     self.bg_rect = self.bg.get_rect() 
        # except Exception as e:
        #     print("Не удалось загрузить кновки:", e)
        #     self.bg_image = None
    def handle_events(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:  # или любая клавиша
                    self.director.switch_scene("creation")
    
    def render(self, screen):
        screen.fill(BLUE)
        screen.blit(self.bg, self.bg_rect)

