import pygame as pg
from config import BROWN, BLACK
from tools.ui_element import UIElement, UIState

class Input_box(UIElement):
    """Поле ввода с системой состояний"""
    
    def __init__(self, image, x, y, font, scale=1, text_color=BROWN, placeholder="", center=True, max_length=20):
        # Масштабируем изображение
        width = image.get_width()
        height = image.get_height()
        self.image = pg.transform.scale(image, (int(width * scale), int(height * scale)))
        
        # Инициализируем базовый класс
        super().__init__(x, y, self.image.get_width(), self.image.get_height())
        
        # Размещаем изображение по координатам
        if center:
            self.rect.center = (x, y)
        else:
            self.rect.topleft = (x, y)
        
        self.text = ""
        self.placeholder = placeholder
        self.font = font
        self.text_color = text_color
        self.placeholder_color = (text_color[0]//2, text_color[1]//2, text_color[2]//2)
        self.center = center
        self.max_length = max_length
        
        # Анимация курсора
        self.cursor_visible = True
        self.cursor_timer = 0
        self.cursor_blink_speed = 0.5  # секунды
        
        # Callbacks
        self.on_submit = None  # Вызывается при нажатии Enter
        self.on_text_change = None  # Вызывается при изменении текста
        
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
        if not self.visible or not self.enabled:
            return False
        
        # Обработка клика
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.focus()
                self.state = UIState.ACTIVE
            else:
                self.unfocus()
                if self.state == UIState.ACTIVE:
                    self.state = UIState.NORMAL
        
        # Обработка ввода текста только если поле в фокусе
        if event.type == pg.KEYDOWN and self._focused:
            if event.key == pg.K_BACKSPACE:
                if self.text:
                    self.text = self.text[:-1]
                    self._update_text_surface()
                    if self.on_text_change:
                        self.on_text_change(self, self.text)
            
            elif event.key == pg.K_RETURN:
                if self.on_submit:
                    self.on_submit(self, self.text)
                return True
            
            elif event.key == pg.K_ESCAPE:
                self.unfocus()
                self.state = UIState.NORMAL
            
            elif len(self.text) < self.max_length and event.unicode.isprintable():
                self.text += event.unicode
                self._update_text_surface()
                if self.on_text_change:
                    self.on_text_change(self, self.text)
        
        return False
    
    def update(self, dt):
        """Обновление состояния поля ввода"""
        super().update(dt)
        
        # Анимация мигания курсора
        if self._focused:
            self.cursor_timer += dt
            if self.cursor_timer >= self.cursor_blink_speed:
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = 0
    
    def draw(self, surface):
        """Отрисовка поля ввода"""
        if not self.visible:
            return
        
        # Рисуем фон с учётом альфа канала
        if self.alpha < 255:
            temp_surface = self.image.copy()
            temp_surface.set_alpha(self.alpha)
            surface.blit(temp_surface, self.rect)
        else:
            surface.blit(self.image, self.rect)
        
        # Рисуем текст
        text_to_draw = self.text_surf.copy()
        if self.alpha < 255:
            text_to_draw.set_alpha(self.alpha)
        surface.blit(text_to_draw, self.text_rect)
        
        # Рисуем курсор если поле активно
        if self._focused and self.cursor_visible:
            cursor_x = self.text_rect.right + 2
            cursor_y = self.text_rect.top
            cursor_color = self.text_color if self.alpha == 255 else (*self.text_color[:3], self.alpha)
            pg.draw.line(surface, cursor_color, 
                        (cursor_x, cursor_y), 
                        (cursor_x, self.text_rect.bottom), 2)
        
        # Визуальная индикация состояния
        if self.state == UIState.ACTIVE or self._focused:
            # Рисуем рамку вокруг активного поля
            pg.draw.rect(surface, self.text_color, self.rect, 2)
        elif self.state == UIState.HOVER:
            # Тонкая рамка при наведении
            pg.draw.rect(surface, self.placeholder_color, self.rect, 1)
    
    def get_text(self):
        """Получить введенный текст"""
        return self.text
    
    def clear(self):
        """Очистить текст"""
        self.text = ""
        self._update_text_surface()
        if self.on_text_change:
            self.on_text_change(self, self.text)
    
    def update_text(self, new_text):
        """Установить текст"""
        self.text = new_text[:self.max_length]
        self._update_text_surface()
    
    def set_position(self, x, y):
        """Изменить позицию поля ввода"""
        super().set_position(x, y)
        if self.center:
            self.rect.center = (x, y)
        else:
            self.rect.topleft = (x, y)
        self._update_text_surface()