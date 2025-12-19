import pygame as pg
from enum import Enum

class UIState(Enum):
    """Состояния UI элемента"""
    NORMAL = "normal"
    HOVER = "hover"
    ACTIVE = "active"
    DISABLED = "disabled"
    HIDDEN = "hidden"

class UIElement:
    """Базовый класс для всех UI элементов с системой состояний"""
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pg.Rect(x, y, width, height)
        
        # Система состояний
        self._state = UIState.NORMAL
        self._enabled = True
        self._visible = True
        self._focused = False
        
        # Callbacks для событий
        self.on_click = None
        self.on_hover_enter = None
        self.on_hover_exit = None
        self.on_state_change = None
        
        # Анимация (альфа канал)
        self.alpha = 255
        self.target_alpha = 255
        self.fade_speed = 5
    
    @property
    def state(self):
        """Получить текущее состояние"""
        return self._state
    
    @state.setter
    def state(self, new_state):
        """Установить новое состояние"""
        if self._state != new_state:
            old_state = self._state
            self._state = new_state
            self._on_state_changed(old_state, new_state)
    
    @property
    def enabled(self):
        """Проверить, активен ли элемент"""
        return self._enabled
    
    @enabled.setter
    def enabled(self, value):
        """Включить/выключить элемент"""
        self._enabled = value
        if not value:
            self.state = UIState.DISABLED
        else:
            self.state = UIState.NORMAL
    
    @property
    def visible(self):
        """Проверить, виден ли элемент"""
        return self._visible
    
    @visible.setter
    def visible(self, value):
        """Показать/скрыть элемент"""
        self._visible = value
        if not value:
            self.state = UIState.HIDDEN
    
    def show(self):
        """Показать элемент с плавным появлением"""
        self._visible = True
        self.state = UIState.NORMAL
        self.alpha = 0
        self.target_alpha = 255
    
    def hide(self):
        """Скрыть элемент с плавным исчезновением"""
        self.target_alpha = 0
    
    def enable(self):
        """Активировать элемент"""
        self.enabled = True
    
    def disable(self):
        """Деактивировать элемент"""
        self.enabled = False
    
    def focus(self):
        """Установить фокус на элемент"""
        self._focused = True
    
    def unfocus(self):
        """Снять фокус с элемента"""
        self._focused = False
    
    def is_hovered(self):
        """Проверить, наведён ли курсор на элемент"""
        if not self._visible or not self._enabled:
            return False
        pos = pg.mouse.get_pos()
        return self.rect.collidepoint(pos)
    
    def handle_event(self, event):
        """Обработка событий (переопределяется в наследниках)"""
        if not self._visible or not self._enabled:
            return False
        
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.state = UIState.ACTIVE
                if self.on_click:
                    self.on_click(self)
                return True
        
        return False
    
    def update(self, dt):
        """Обновление состояния элемента"""
        if not self._visible:
            return
        
        # Обновляем состояние наведения
        if self._enabled:
            is_hovered = self.is_hovered()
            
            if is_hovered and self.state == UIState.NORMAL:
                self.state = UIState.HOVER
                if self.on_hover_enter:
                    self.on_hover_enter(self)
            elif not is_hovered and self.state == UIState.HOVER:
                self.state = UIState.NORMAL
                if self.on_hover_exit:
                    self.on_hover_exit(self)
        
        # Плавная анимация альфа канала
        if self.alpha < self.target_alpha:
            self.alpha = min(self.alpha + self.fade_speed, self.target_alpha)
        elif self.alpha > self.target_alpha:
            self.alpha = max(self.alpha - self.fade_speed, self.target_alpha)
        
        # Скрываем элемент после исчезновения
        if self.alpha == 0 and self.target_alpha == 0:
            self._visible = False
    
    def draw(self, surface):
        """Отрисовка элемента (переопределяется в наследниках)"""
        if not self._visible:
            return
    
    def set_position(self, x, y):
        """Установить позицию элемента"""
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
    
    def set_size(self, width, height):
        """Установить размер элемента"""
        self.width = width
        self.height = height
        self.rect.width = width
        self.rect.height = height
    
    def _on_state_changed(self, old_state, new_state):
        """Вызывается при изменении состояния"""
        if self.on_state_change:
            self.on_state_change(self, old_state, new_state)
    
    def get_state_color(self, normal_color, hover_color=None, active_color=None, disabled_color=None):
        """Получить цвет в зависимости от состояния"""
        if self.state == UIState.DISABLED and disabled_color:
            return disabled_color
        elif self.state == UIState.ACTIVE and active_color:
            return active_color
        elif self.state == UIState.HOVER and hover_color:
            return hover_color
        return normal_color