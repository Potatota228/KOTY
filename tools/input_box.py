# input_box.py
import pygame as pg
from config import BROWN, BLACK

class Input_box():
    def __init__(self, image, x, y, font, scale=1, text_color=BROWN, placeholder="", center=True, max_length=20):
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
        
        self.text = ""
        self.placeholder = placeholder
        self.font = font
        self.text_color = text_color
        self.placeholder_color = (text_color[0]//2, text_color[1]//2, text_color[2]//2)  # Более тусклый цвет
        self.center = center
        self.active = False
        self.max_length = max_length
        
        self._update_text_surface()
    
    def _update_text_surface(self):
        """Обновить поверхность текста"""
        if self.text:
            self.text_surf = self.font.render(self.text, True, self.text_color)
        else:
            self.text_surf = self.font.render(self.placeholder, True, self.placeholder_color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
    
    def handle_event(self, event):
        """Обработка событий ввода"""
        if event.type == pg.MOUSEBUTTONDOWN:
            # Проверяем клик по полю
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
        
        if event.type == pg.KEYDOWN and self.active:
            if event.key == pg.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pg.K_RETURN:
                return True  # Возвращаем True при нажатии Enter
            elif len(self.text) < self.max_length:
                self.text += event.unicode
            self._update_text_surface()
        
        return False
    
    def draw(self, surface):
        """Отрисовка поля ввода"""
        surface.blit(self.image, self.rect)
        surface.blit(self.text_surf, self.text_rect)
        
        # Рисуем курсор если поле активно
        if self.active:
            cursor_x = self.text_rect.right + 2
            cursor_y = self.text_rect.top
            pg.draw.line(surface, self.text_color, 
                        (cursor_x, cursor_y), 
                        (cursor_x, self.text_rect.bottom), 2)
    
    def get_text(self):
        """Получить введенный текст"""
        return self.text
    
    def clear(self):
        """Очистить текст"""
        self.text = ""
        self._update_text_surface()
    
    def update_text(self, new_text):
        """Установить текст"""
        self.text = new_text[:self.max_length]
        self._update_text_surface()
    
    def set_position(self, x, y):
        """Изменить позицию поля ввода"""
        self.x = x
        self.y = y
        if self.center:
            self.rect.center = (x, y)
        else:
            self.rect.topleft = (x, y)
        self._update_text_surface()