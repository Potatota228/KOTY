import pygame as pg
from Scenes.scene import Scene
from config import BEIGE, BROWN
from tools.text_box import Text_box

class CreationScene(Scene):
    """Сцена создания клана"""
    
    def __init__(self, director):
        super().__init__(director)
        self._setup_ui()
    
    def _setup_ui(self):
        """Настройка UI элементов"""
        # Загружаем изображения из менеджера ресурсов
        self.bg_img = self.resource_manager.get_image("clan_four_light")
        if self.bg_img:
            self.bg_img.set_colorkey(BROWN)
            self.bg_rect = self.bg_img.get_rect()
        else:
            self.bg_rect = None
        
        self.frame_img = self.resource_manager.get_image("clan_name_frame")
        self.frame_rect = self.frame_img.get_rect() if self.frame_img else None
        
        # Получаем шрифт
        font = self.resource_manager.get_font("main", 20)
        
        # Создаём текстовое поле
        self.title = Text_box(
            self.frame_img, 
            400, 100, 
            "Привет, мир!", 
            font, 
            text_color=(255, 255, 255)
        )
    
    def on_enter(self):
        """Вызывается при входе в сцену"""
        print("Вход в сцену создания")
    
    def handle_events(self, events):
        """Обработка событий"""
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.director.switch_scene("menu")
                elif event.key == pg.K_ESCAPE:
                    self.director.switch_scene("menu")
    
    def update(self, dt):
        """Обновление логики"""
        pass
    
    def render(self, screen):
        """Отрисовка сцены"""
        screen.fill(BEIGE)
        
        # Рисуем фон снизу
        if self.bg_img and self.bg_rect:
            self.bg_rect.bottom = screen.get_height()
            screen.blit(self.bg_img, self.bg_rect)
        
        # Рисуем рамку сверху
        if self.frame_img and self.frame_rect:
            self.frame_rect.top = screen.get_height() - 10
            screen.blit(self.frame_img, self.frame_rect)
        
        # Рисуем текстовое поле
        self.title.draw(screen)