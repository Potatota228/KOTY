import pygame as pg
import os
class MenuScene(Scene):
    def __init__(self, director):
        super().__init__(director)
        current_dir = os.path.dirname(__file__)
        parent_dir = os.path.dirname(current_dir)
        bg_path = os.path.join(parent_dir, "menu_logoless.png")
        try:
            self.bg_image = pg.image.load(bg_path).convert()
            screen_size = director.screen.get_size()
            self.bg_image = pg.transform.scale(self.bg_image, screen_size())
        except Exception as e:
            print("Не удалось загрузить фоновое изображение: ", e)
            self.bg_image = None
    
    def handle_events(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:  # или любая клавиша
                    self.director.switch_scene("creation")
    
    def render(self, screen):
        screen.fill(BLUE)
        if self.bg_image:
            screen.blit(self.bg_image, (0, 0))
        else:
            screen.fill(BLUE)



