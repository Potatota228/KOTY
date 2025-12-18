import pygame as pg
from Scenes.scene import Scene
from config import BLUE
from tools.button import Button

class MenuScene(Scene):
    """Главное меню игры"""
    
    def __init__(self, director):
        super().__init__(director)
        self._setup_ui()
    
    def _setup_ui(self):
        """Настройка UI элементов"""
        # Фоновое изображение
        self.bg_image = self.resource_manager.get_image("menu_bg")
        self.bg_rect = self.bg_image.get_rect() if self.bg_image else None
        
        # Получаем шрифт и изображение кнопки
        font = self.resource_manager.get_font("main", 20)
        bt_img = self.resource_manager.get_image("button")
        
        # Создаём кнопки
        self.bt_start = Button(50, 400, bt_img, 1, "Start", font, center=False)
        self.bt_infobox = Button(50, 500, bt_img, 1, "Info", font, center=False)
        
        # Добавляем кнопки в список UI элементов для удобства
        self.buttons = [self.bt_start, self.bt_infobox]
    
    def on_enter(self):
        """Вызывается при входе в сцену"""
        print("Вход в главное меню")
    
    def handle_events(self, events):
        """Обработка событий"""
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.director.switch_scene("creation")
                elif event.key == pg.K_ESCAPE:
                    self.director.quit()
    
    def update(self, dt):
        """Обновление логики (пока пусто)"""
        pass
    
    def render(self, screen):
        """Отрисовка сцены"""
        screen.fill(BLUE)
        
        # Рисуем фон
        if self.bg_image and self.bg_rect:
            screen.blit(self.bg_image, self.bg_rect)
        
        # Проверяем нажатия кнопок и рисуем их
        if self.bt_start.draw(screen):
            self.director.switch_scene("creation")
        
        if self.bt_infobox.draw(screen):
            self.director.switch_scene("infobox")