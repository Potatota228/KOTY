import pygame as pg
from .scene import Scene
from config import BLUE
from tools.buttons import Button
class MenuScene(Scene):
    def __init__(self, director):
        super().__init__(director)
        font = pg.font.Font("Comic Sans MS.ttf", 32)
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
            self.bt_start = Button(50, 400, bt_img, 1, "text", font)
        except Exception as e:
            print("Не удалось загрузить кновки:", e)
            self.bg_image = None
    def handle_events(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:  # или любая клавиша
                    self.director.switch_scene("creation")
    
    def render(self, screen):
        screen.fill(BLUE)
        screen.blit(self.bg_image, self.bg_rect)
        if self.bt_start.draw(screen):
            self.director.switch_scene("creation")
        self.bt_start.blit(self.text, (0, 0))
        

