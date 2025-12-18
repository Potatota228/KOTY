import pygame as pg
from Scenes.scene import Scene
from config import WHITE, font
from tools.button import Button

class InfoBoxScene(Scene):
    def __init__(self, director):
        super().__init__(director)
        self.buttons = []
        try:
            bt_path = "./images/buttons/button.png"
            bt_img = pg.image.load(bt_path).convert_alpha()
            # Добавляем center=False
            self.bt_back = Button(50, 600, bt_img, 1, "Back", font, center=False)
            
        except Exception as e:
            print("Не удалось загрузить кнопки:", e)
            self.bg_image = None
        
    def handle_events(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.director.switch_scene("menu")
    
    def render(self, screen):
        screen.fill(WHITE)
        if self.bt_back.draw(screen):
            self.director.switch_scene("menu")

    def cleanup(self):
        self.buttons.clear()
        self.bt_back = None  # Исправлено с bt_start на bt_back