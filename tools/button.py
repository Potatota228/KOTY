import pygame as pg
from config import BLACK
from tools.ui_element import UIElement, UIState

class Button(UIElement):
    """
    Кнопка с изображением и текстом
    
    Наследуется от UIElement, получая систему состояний и анимации
    """
    
    def __init__(self, x, y, image, scale, text, font, text_color=BLACK, center=True):
        """
        Args:
            x, y: координаты кнопки
            image: pygame Surface с изображением кнопки
            scale: масштаб (1.0 = оригинальный размер)
            text: текст на кнопке
            font: pygame Font для текста
            text_color: цвет текста
            center: если True, x,y — это центр, иначе — верхний левый угол
        """
        # Масштабируем изображение
        width = image.get_width()
        height = image.get_height()
        self.image = pg.transform.scale(image, (int(width * scale), int(height * scale)))
        
        # Инициализируем базовый класс
        super().__init__(x, y, self.image.get_width(), self.image.get_height())
        
        self.center = center
        self.text = text
        self.font = font
        self.text_color = text_color
        
        # Размещаем кнопку
        if center:
            self.rect.center = (x, y)
        else:
            self.rect.topleft = (x, y)
        
        # Состояние нажатия (для обратной совместимости)
        self.clicked = False
        
        # Создаём текстовую поверхность
        self._update_text_surface()
    
    def _update_text_surface(self):
        """Создать/обновить поверхность с текстом"""
        self.text_surf = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
    
    def handle_event(self, event):
        """
        Обработка событий кнопки
        
        Args:
            event: pygame событие
            
        Returns:
            True если кнопка была нажата
        """
        if not self.visible or not self.enabled:
            return False
        
        # Обрабатываем клик
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.state = UIState.ACTIVE
                if self.on_click:
                    self.on_click(self)
                return True
        
        # Сбрасываем состояние при отпускании кнопки мыши
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            if self.state == UIState.ACTIVE:
                self.state = UIState.HOVER if self.is_hovered() else UIState.NORMAL
        
        return False
    
    def draw(self, surface):
        """
        Отрисовка кнопки (старый метод для обратной совместимости)
        
        Возвращает True если кнопка была нажата В ЭТОМ КАДРЕ
        Это позволяет использовать кнопку в стиле:
        if button.draw(screen):
            # действие при нажатии
        """
        if not self.visible:
            return False
        
        action = False
        pos = pg.mouse.get_pos()

        # Проверяем нажатие (старая логика)
        if self.rect.collidepoint(pos) and self.enabled:
            if pg.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                action = True

        if not pg.mouse.get_pressed()[0]:
            self.clicked = False

        # Рисуем изображение кнопки с учётом альфа канала
        
        if self.alpha < 255:
            temp_image = self.image.copy()
            temp_image.set_alpha(self.alpha)
            surface.blit(temp_image, self.rect)
        else:
            surface.blit(self.image, self.rect)

        # Рисуем текст
        # Если кнопка неактивна, делаем текст полупрозрачным
        if self.state == UIState.DISABLED:
            text_to_draw = self.text_surf.copy()
            text_to_draw.set_alpha(128)  # 50% прозрачности
            surface.blit(text_to_draw, self.text_rect)
        else:
            if self.alpha < 255:
                text_to_draw = self.text_surf.copy()
                text_to_draw.set_alpha(self.alpha)
                surface.blit(text_to_draw, self.text_rect)
            else:
                surface.blit(self.text_surf, self.text_rect)

        # # Визуальная индикация состояния
        # if self.state == UIState.HOVER and self.enabled:
        #     # Затемнение при наведении
        #     darken = pg.Surface(self.rect.size, pg.SRCALPHA)
        #     darken.fill((0, 0, 0, 60))  # Чёрный с прозрачностью
        #     surface.blit(darken, self.rect.topleft)

        return action
    
    def update_text(self, new_text):
        """
        Обновить текст на кнопке
        
        Args:
            new_text: новый текст
        """
        self.text = new_text
        self._update_text_surface()
    
    def set_position(self, x, y):
        """
        Изменить позицию кнопки
        
        Args:
            x, y: новые координаты
        """
        super().set_position(x, y)
        
        if self.center:
            self.rect.center = (x, y)
        else:
            self.rect.topleft = (x, y)
        
        # Обновляем позицию текста относительно кнопки
        self.text_rect.center = self.rect.center