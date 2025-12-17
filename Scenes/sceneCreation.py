import pygame as pg
from .scene import Scene
from config import BEIGE, BROWN, font
from tools.buttons import Button
from tools.text_boxes import Text
class CreationScene(Scene):
    def __init__(self, director):
        super().__init__(director)
        try:
            bg_path = "./images/clan_four_light.png"
            self.bg_image = pg.image.load(bg_path).convert_alpha()
            self.bg_image.set_colorkey(BROWN)
            self.bg_rect = self.bg_image.get_rect()
        except Exception as e:
            print("Не удалось загрузить фоновое изображение:", e)
            self.bg_image = None

        self.title = Text(400, 100, "Привет, мир!", pg.font.Font(None, 48), (255, 255, 255))
    def handle_events(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:  # или любая клавиша
                    self.director.switch_scene("menu")
    
    def render(self, screen):
        screen.fill(BEIGE)
        self.bg_rect.bottom = screen.get_height()
        screen.blit(self.bg_image, self.bg_rect)
        self.title.draw(screen)
        

