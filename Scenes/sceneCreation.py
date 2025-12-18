import pygame as pg
from .scene import Scene
from config import BEIGE, BROWN, font
from tools.button import Button
from tools.text_box import Text_box

class CreationScene(Scene):
    def __init__(self, director):
        super().__init__(director)
        try:
            bg_path = "./images/clan_four_light.png"
            self.bg_img = pg.image.load(bg_path).convert_alpha()
            self.bg_img.set_colorkey(BROWN)
            self.bg_rect = self.bg_img.get_rect()

            img_path = "./images/clan_name_frame.png"
            self.img = pg.image.load(img_path).convert_alpha()
            self.img_rect = self.img.get_rect()

        except Exception as e:
            print("Не удалось загрузить фоновое изображение:", e)
            self.bg_img = None

        # Передаем self.img (загруженное изображение), а не строку
        self.title = Text_box(self.img, 400, 100, "Привет, мир!", font, text_color=(255, 255, 255))
    
    def handle_events(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:  # или любая клавиша
                    self.director.switch_scene("menu")
    
    def render(self, screen):
        screen.fill(BEIGE)

        # Исправлено: self.bg_img вместо self.bg_image
        self.bg_rect.bottom = screen.get_height()
        screen.blit(self.bg_img, self.bg_rect)

        # Исправлено: используем self.img_rect.top
        self.img_rect.top = (screen.get_height() - 10)
        screen.blit(self.img, self.img_rect)
        
        # Отрисовываем text_box
        self.title.draw(screen)