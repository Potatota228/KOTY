import pygame as pg

class Scene:
    """Базовый класс для всех сцен"""
    
    def __init__(self, director):
        self.director = director
        self.resource_manager = director.resource_manager
        self.ui_elements = []
        
    def on_enter(self):
        """Вызывается при входе в сцену"""
        pass
    
    def on_exit(self):
        """Вызывается при выходе из сцены"""
        pass
    
    def handle_events(self, events):
        """Обработка событий"""
        pass
    
    def update(self, dt):
        """Обновление логики сцены"""
        pass
    
    def render(self, screen):
        """Отрисовка сцены"""
        pass
    
    def add_ui_element(self, element):
        """Добавить UI элемент для автоматической отрисовки"""
        self.ui_elements.append(element)
    
    def draw_ui_elements(self, screen):
        """Отрисовка всех UI элементов"""
        for element in self.ui_elements:
            element.draw(screen)
    
    def clear_ui_elements(self):
        """Очистка UI элементов"""
        self.ui_elements.clear()