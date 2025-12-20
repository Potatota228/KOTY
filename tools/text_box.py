import pygame as pg
from config import BROWN
from tools.ui_element import UIElement, UIState

class Text_box(UIElement):
    """
    Текст с фоновым изображением
    
    Наследуется от UIElement для поддержки анимаций и состояний
    """
    
    def __init__(self, image, x, y, text, font, scale=1, text_color=BROWN, center=True):
        """
        Args:
            image: pygame Surface с фоновым изображением
            x, y: координаты текстового блока
            text: содержимое текста
            font: pygame Font для отрисовки
            scale: масштаб изображения (1.0 = оригинальный размер)
            text_color: цвет текста (RGB tuple)
            center: если True, x,y — это центр, иначе — левый верхний угол
        """
        # Масштабируем изображение
        width = image.get_width()
        height = image.get_height()
        self.image = pg.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        
        self.x = x
        self.y = y
        self.center = center
        
        # Размещаем изображение по координатам
        if center:
            self.rect.center = (x, y)
        else:
            self.rect.topleft = (x, y)
        
        self.text = text
        self.font = font
        self.text_color = text_color
        
        # Создаём текстовую поверхность
        self.text_surf = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect()
        
        # Размещаем текст по центру изображения
        self.text_rect.center = self.rect.center
        
        # Инициализируем базовый класс
        super().__init__(
            self.rect.x,
            self.rect.y,
            self.rect.width,
            self.rect.height
        )
    
    def update_text(self, new_text):
        """
        Обновить текст
        
        Args:
            new_text: новое содержимое текста
        """
        self.text = new_text
        self.text_surf = self.font.render(self.text, True, self.text_color)
        # Текст всегда по центру коробки
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
    
    def set_position(self, x, y):
        """
        Изменить позицию текстового блока
        
        Args:
            x, y: новые координаты
        """
        self.x = x
        self.y = y
        
        if self.center:
            self.rect.center = (x, y)
        else:
            self.rect.topleft = (x, y)
        
        # Обновляем позицию текста относительно коробки
        self.text_rect.center = self.rect.center
        
        # Синхронизируем с базовым классом
        super().set_position(self.rect.x, self.rect.y)
    
    def draw(self, surface):
        """
        Отрисовка текстового блока
        
        Args:
            surface: pygame Surface на которой рисуем
        """
        # Проверяем видимость
        if not self.visible:
            return
        
        # Рисуем фон с учётом прозрачности
        if self.alpha < 255:
            temp_image = self.image.copy()
            temp_image.set_alpha(self.alpha)
            surface.blit(temp_image, self.rect)
            
            temp_text = self.text_surf.copy()
            temp_text.set_alpha(self.alpha)
            surface.blit(temp_text, self.text_rect)
        else:
            surface.blit(self.image, self.rect)
            surface.blit(self.text_surf, self.text_rect)
    
    def handle_event(self, event):
        """
        Text_box не обрабатывает события (это просто метка с фоном)
        
        Args:
            event: pygame событие
            
        Returns:
            False — не обрабатывает события
        """
        return False