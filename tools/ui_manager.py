import pygame as pg
from collections import defaultdict

class UIManager:
    """Менеджер для управления группами UI элементов"""
    
    def __init__(self):
        self.elements = []
        self.groups = defaultdict(list)
        self.focused_element = None
    
    def add(self, element, group=None):
        """Добавить UI элемент"""
        if element not in self.elements:
            self.elements.append(element)
            if group:
                self.groups[group].append(element)
    
    def remove(self, element):
        """Удалить UI элемент"""
        if element in self.elements:
            self.elements.remove(element)
            # Удаляем из всех групп
            for group_elements in self.groups.values():
                if element in group_elements:
                    group_elements.remove(element)
    
    def get_group(self, group_name):
        """Получить элементы группы"""
        return self.groups.get(group_name, [])
    
    def show_group(self, group_name):
        """Показать все элементы группы"""
        for element in self.groups.get(group_name, []):
            element.show()
    
    def hide_group(self, group_name):
        """Скрыть все элементы группы"""
        for element in self.groups.get(group_name, []):
            element.hide()
    
    def enable_group(self, group_name):
        """Активировать все элементы группы"""
        for element in self.groups.get(group_name, []):
            element.enable()
    
    def disable_group(self, group_name):
        """Деактивировать все элементы группы"""
        for element in self.groups.get(group_name, []):
            element.disable()
    
    def handle_events(self, events):
        """Обработка событий для всех элементов"""
        for event in events:
            for element in self.elements:
                if element.handle_event(event):
                    # Элемент обработал событие
                    break
    
    def update(self, dt):
        """Обновление всех элементов"""
        for element in self.elements:
            element.update(dt)
    
    def draw(self, surface):
        """Отрисовка всех элементов"""
        for element in self.elements:
            element.draw(surface)
    
    def clear(self):
        """Очистить все элементы"""
        self.elements.clear()
        self.groups.clear()
        self.focused_element = None
    
    def clear_group(self, group_name):
        """Очистить группу элементов"""
        if group_name in self.groups:
            for element in self.groups[group_name]:
                if element in self.elements:
                    self.elements.remove(element)
            del self.groups[group_name]