import pygame as pg
from tools.ui_manager import UIManager

class Scene:
    """
    Базовый класс для всех сцен игры
    
    Каждая сцена — это отдельный "экран" игры (меню, создание персонажа и т.д.)
    Сцена управляет своими UI элементами через UIManager
    """
    
    def __init__(self, director):
        """
        Args:
            director: главный контроллер игры, связывает все сцены
        """
        self.director = director
        self.resource_manager = director.resource_manager
        
        # UI Manager для управления всеми элементами интерфейса
        self.ui_manager = UIManager()
    
    def on_enter(self):
        """
        Вызывается когда игрок переходит НА эту сцену
        Здесь инициализируем элементы, запускаем музыку и т.д.
        """
        pass
    
    def on_exit(self):
        """
        Вызывается когда игрок УХОДИТ с этой сцены
        Здесь останавливаем музыку, сохраняем данные и т.д.
        """
        pass
    
    def handle_events(self, events):
        """
        Обработка событий (клики мыши, нажатия клавиш)
        
        Args:
            events: список событий pygame (pg.MOUSEBUTTONDOWN, pg.KEYDOWN и т.д.)
        """
        # Передаём все события в UI Manager
        # Он сам разберётся какой элемент должен их обработать
        self.ui_manager.handle_events(events)
    
    def update(self, dt):
        """
        Обновление логики сцены каждый кадр
        
        Args:
            dt: delta time — время с прошлого кадра в секундах
                Нужен для плавной анимации независимо от FPS
                Пример: position += speed * dt
        """
        self.ui_manager.update(dt)
    
    def render(self, screen):
        """
        Отрисовка сцены на экране
        
        Args:
            screen: главная Surface pygame, на которой рисуем
        """
        # В конце всегда рисуем UI поверх всего остального
        self.ui_manager.draw(screen)
    
    # === Вспомогательные методы для работы с UI ===
    
    def add_ui(self, element, group=None):
        """
        Добавить UI элемент в сцену
        
        Args:
            element: любой UI элемент (Button, Input_box и т.д.)
            group: имя группы для организации элементов (опционально)
        """
        self.ui_manager.add(element, group)
    
    def remove_ui(self, element):
        """Удалить UI элемент из сцены"""
        self.ui_manager.remove(element)
    
    def show_group(self, group_name):
        """Показать все элементы группы"""
        self.ui_manager.show_group(group_name)
    
    def hide_group(self, group_name):
        """Скрыть все элементы группы"""
        self.ui_manager.hide_group(group_name)
    
    def clear_ui(self):
        """Очистить все UI элементы (полезно при смене сцены)"""
        self.ui_manager.clear()