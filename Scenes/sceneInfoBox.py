import pygame as pg
from Scenes.scene import Scene
from config import WHITE
from tools.button import Button

class InfoBoxScene(Scene):
    """Сцена с информацией"""
    
    def __init__(self, director):
        super().__init__(director)
        self._setup_ui()
    
    def _setup_ui(self):
        """Настройка UI элементов"""
        font = self.resource_manager.get_font("main", 20)
        bt_img = self.resource_manager.get_image("button")
        
        # Создаём кнопку возврата
        self.bt_back = Button(50, 600, bt_img, 1, "Back", font, center=False)
    
    def on_enter(self):
        """Вызывается при входе в сцену"""
        print("Вход в информационную сцену")
    
    def handle_events(self, events):
        """Обработка событий"""
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE or event.key == pg.K_ESCAPE:
                    self.director.switch_scene("menu")
    
    def update(self, dt):
        """Обновление логики"""
        pass
    
    def render(self, screen):
        """Отрисовка сцены"""
        screen.fill(WHITE)
        
        # Проверяем нажатие и рисуем кнопку
        if self.bt_back.draw(screen):
            self.director.switch_scene("menu")