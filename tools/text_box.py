import pygame as pg
from config import BROWN

class Text_box():
    def __init__(self, image, x, y, text, font, scale=1, text_color=BROWN, center=True):
        self.x = x
        self.y = y
        width = image.get_width()
        height = image.get_height()
        self.image = pg.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        
        # Размещаем изображение по координатам
        if center:
            self.rect.center = (x, y)
        else:
            self.rect.topleft = (x, y)
        
        self.text = text
        self.font = font
        self.text_color = text_color
        self.center = center
        
        self.text_surf = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect()
        
        # Размещаем текст по центру изображения
        self.text_rect.center = self.rect.center
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        surface.blit(self.text_surf, self.text_rect)
    
    def update_text(self, new_text):
        """Обновить текст"""
        self.text = new_text
        self.text_surf = self.font.render(self.text, True, self.text_color)
        # Текст всегда по центру коробки
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
    
    def set_position(self, x, y):
        """Изменить позицию текста и коробки"""
        self.x = x
        self.y = y
        if self.center:
            self.rect.center = (x, y)
        else:
            self.rect.topleft = (x, y)
        # Обновляем позицию текста относительно коробки
        self.text_rect.center = self.rect.center