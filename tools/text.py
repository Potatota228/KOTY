import pygame as pg
from config import BROWN
from tools.ui_element import UIElement, UIState

class Text(UIElement):
    """
    Текстовая метка с поддержкой системы состояний
    
    Теперь наследуется от UIElement и получает все его возможности:
    - Показать/скрыть с анимацией
    - Управление видимостью
    - Плавное появление/исчезновение
    """
    
    def __init__(self, x, y, text, font, text_color=BROWN, center=True):
        """
        Args:
            x, y: координаты текста
            text: содержимое текста
            font: pygame Font для отрисовки
            text_color: цвет текста (RGB tuple)
            center: если True, x,y — это центр текста, иначе — левый верхний угол
        """
        self.text = text
        self.font = font
        self.text_color = text_color
        self.center = center
        
        # Создаём поверхность с текстом
        self.text_surf = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect()
        
        # Размещаем текст по координатам
        if center:
            self.text_rect.center = (x, y)
        else:
            self.text_rect.topleft = (x, y)
        
        # Инициализируем базовый класс UIElement
        # Передаём позицию и размеры текста
        super().__init__(
            self.text_rect.x, 
            self.text_rect.y,
            self.text_rect.width,
            self.text_rect.height
        )
        
        # Обновляем rect чтобы совпадал с text_rect
        self.rect = self.text_rect
    
    def update_text(self, new_text):
        """
        Обновить текст
        
        Args:
            new_text: новое содержимое текста
        """
        self.text = new_text
        
        # Создаём новую поверхность с обновлённым текстом
        self.text_surf = self.font.render(self.text, True, self.text_color)
        
        # Получаем старый центр/позицию
        if self.center:
            old_center = self.text_rect.center
            self.text_rect = self.text_surf.get_rect(center=old_center)
        else:
            old_topleft = self.text_rect.topleft
            self.text_rect = self.text_surf.get_rect(topleft=old_topleft)
        
        # Обновляем размеры
        self.rect = self.text_rect
        self.width = self.text_rect.width
        self.height = self.text_rect.height
    
    def set_position(self, x, y):
        """
        Изменить позицию текста
        
        Args:
            x, y: новые координаты
        """
        self.x = x
        self.y = y
        
        if self.center:
            self.text_rect.center = (x, y)
        else:
            self.text_rect.topleft = (x, y)
        
        # Синхронизируем rect
        self.rect = self.text_rect
    
    def draw(self, surface):
        """
        Отрисовка текста
        
        Args:
            surface: pygame Surface на которой рисуем
        """
        # Проверяем видимость
        if not self.visible:
            return
        
        # Рисуем текст с учётом прозрачности (альфа канала)
        if self.alpha < 255:
            # Создаём временную поверхность с прозрачностью
            temp_surf = self.text_surf.copy()
            temp_surf.set_alpha(self.alpha)
            surface.blit(temp_surf, self.text_rect)
        else:
            # Обычная отрисовка
            surface.blit(self.text_surf, self.text_rect)
    
    def handle_event(self, event):
        """
        Text не обрабатывает события (это просто метка)
        Но метод нужен для совместимости с UIManager
        
        Args:
            event: pygame событие
            
        Returns:
            False — текст не обрабатывает события
        """
        return False