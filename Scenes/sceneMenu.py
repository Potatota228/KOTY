import pygame as pg
from .scene import Scene
from config import BLUE, font
from tools.button import Button

class MenuScene(Scene):
    def __init__(self, director):
        super().__init__(director)
        try:
            bg_path = "./images/menu.png"
            self.bg_image = pg.image.load(bg_path).convert_alpha()
            self.bg_rect = self.bg_image.get_rect()
        except Exception as e:
            print("Не удалось загрузить фоновое изображение:", e)
            self.bg_image = None
        try:
            bt_path = "./images/buttons/button.png"
            bt_img = pg.image.load(bt_path).convert_alpha()
            # Добавляем center=False для позиционирования по topleft
            self.bt_start = Button(50, 400, bt_img, 1, "Start", font, center=False)
            self.bt_infobox = Button(50, 500, bt_img, 1, "Info", font, center=False)
        except Exception as e:
            print("Не удалось загрузить кнопки:", e)
            self.bg_image = None
    
    def handle_events(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.director.switch_scene("creation")
    
    def render(self, screen):
        screen.fill(BLUE)
        screen.blit(self.bg_image, self.bg_rect)
        if self.bt_start.draw(screen):
            self.director.switch_scene("creation")
        if self.bt_infobox.draw(screen):
            self.director.switch_scene("infobox")