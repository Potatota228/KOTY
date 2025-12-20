"""
Примеры использования улучшенной системы UI
Этот файл содержит практические примеры для разных ситуаций
"""

import pygame as pg
from Scenes.scene import Scene
from tools.button import Button
from tools.text import Text
from tools.input_box import Input_box
from config import WHITE, BLACK

# ============================================================================
# ПРИМЕР 1: Простая сцена с одной кнопкой
# ============================================================================

class SimpleScene(Scene):
    """Минимальная сцена с одной кнопкой"""
    
    def __init__(self, director):
        super().__init__(director)
        
        # Загружаем ресурсы
        font = self.resource_manager.get_font("main", 20)
        button_img = self.resource_manager.get_image("button")
        
        # Создаём кнопку
        self.button = Button(400, 300, button_img, 1, "Click Me", font)
        
        # Устанавливаем callback
        self.button.on_click = self._on_button_click
        
        # Добавляем в UI Manager
        self.add_ui(self.button)
    
    def _on_button_click(self, button):
        """Вызывается при нажатии кнопки"""
        print("Кнопка нажата!")
        self.director.switch_scene("menu")
    
    def render(self, screen):
        screen.fill(WHITE)
        super().render(screen)  # Рисует все UI элементы


# ============================================================================
# ПРИМЕР 2: Меню с несколькими кнопками и группами
# ============================================================================

class AdvancedMenuScene(Scene):
    """Меню с группами кнопок"""
    
    def __init__(self, director):
        super().__init__(director)
        self._setup_ui()
    
    def _setup_ui(self):
        font = self.resource_manager.get_font("main", 20)
        button_img = self.resource_manager.get_image("button")
        
        # === ГЛАВНОЕ МЕНЮ ===
        self.btn_play = Button(400, 200, button_img, 1, "Play", font)
        self.btn_settings = Button(400, 280, button_img, 1, "Settings", font)
        self.btn_quit = Button(400, 360, button_img, 1, "Quit", font)
        
        # Добавляем в группу "main"
        self.add_ui(self.btn_play, group="main")
        self.add_ui(self.btn_settings, group="main")
        self.add_ui(self.btn_quit, group="main")
        
        # === МЕНЮ НАСТРОЕК (скрыто по умолчанию) ===
        self.btn_volume = Button(400, 200, button_img, 1, "Volume", font)
        self.btn_controls = Button(400, 280, button_img, 1, "Controls", font)
        self.btn_back = Button(400, 360, button_img, 1, "Back", font)
        
        # Добавляем в группу "settings"
        self.add_ui(self.btn_volume, group="settings")
        self.add_ui(self.btn_controls, group="settings")
        self.add_ui(self.btn_back, group="settings")
        
        # Скрываем настройки
        self.hide_group("settings")
        
        # Устанавливаем callbacks
        self.btn_settings.on_click = lambda btn: self._show_settings()
        self.btn_back.on_click = lambda btn: self._show_main()
        self.btn_quit.on_click = lambda btn: self.director.quit()
    
    def _show_settings(self):
        """Показать меню настроек"""
        self.hide_group("main")
        self.show_group("settings")
    
    def _show_main(self):
        """Показать главное меню"""
        self.hide_group("settings")
        self.show_group("main")
    
    def render(self, screen):
        screen.fill(WHITE)
        super().render(screen)


# ============================================================================
# ПРИМЕР 3: Форма с несколькими полями ввода
# ============================================================================

class RegistrationScene(Scene):
    """Форма регистрации с валидацией"""
    
    def __init__(self, director):
        super().__init__(director)
        self._setup_ui()
    
    def _setup_ui(self):
        font = self.resource_manager.get_font("main", 20)
        frame_img = self.resource_manager.get_image("clan_name_frame")
        button_img = self.resource_manager.get_image("button")
        
        # === ЗАГОЛОВКИ ===
        self.title = Text(400, 100, "Create Your Character", font)
        self.label_name = Text(200, 200, "Name:", font, center=False)
        self.label_clan = Text(200, 280, "Clan:", font, center=False)
        
        # === ПОЛЯ ВВОДА ===
        self.input_name = Input_box(frame_img, 400, 200, font, max_length=15)
        self.input_clan = Input_box(frame_img, 400, 280, font, max_length=20)
        
        # Callbacks для валидации
        self.input_name.on_text_change = self._validate_form
        self.input_clan.on_text_change = self._validate_form
        
        # === КНОПКИ ===
        self.btn_submit = Button(400, 400, button_img, 1, "Create", font)
        self.btn_submit.enabled = False  # Изначально неактивна
        self.btn_submit.on_click = self._on_submit
        
        self.btn_cancel = Button(400, 480, button_img, 1, "Cancel", font)
        self.btn_cancel.on_click = lambda btn: self.director.switch_scene("menu")
        
        # Добавляем всё в UI Manager
        for element in [self.title, self.label_name, self.label_clan,
                       self.input_name, self.input_clan, 
                       self.btn_submit, self.btn_cancel]:
            self.add_ui(element)
    
    def _validate_form(self, input_box, text):
        """Проверяем заполнены ли все поля"""
        name_filled = len(self.input_name.get_text().strip()) >= 2
        clan_filled = len(self.input_clan.get_text().strip()) >= 3
        
        # Активируем кнопку только если оба поля заполнены
        self.btn_submit.enabled = name_filled and clan_filled
    
    def _on_submit(self, button):
        """Обработка отправки формы"""
        name = self.input_name.get_text()
        clan = self.input_clan.get_text()
        
        print(f"Создан персонаж: {name} из клана {clan}")
        
        # Переходим в игру, передавая данные
        self.director.switch_scene("game", player_name=name, clan=clan)
    
    def on_enter(self):
        # Ставим фокус на первое поле
        self.input_name.focus()
    
    def render(self, screen):
        screen.fill(WHITE)
        super().render(screen)


# ============================================================================
# ПРИМЕР 4: Анимированное появление меню
# ============================================================================

class AnimatedMenuScene(Scene):
    """Меню с плавным появлением кнопок"""
    
    def __init__(self, director):
        super().__init__(director)
        self._setup_ui()
    
    def _setup_ui(self):
        font = self.resource_manager.get_font("main", 24)
        button_img = self.resource_manager.get_image("button")
        
        # Создаём кнопки с задержкой появления
        buttons_data = [
            ("New Game", 200, 0.0),     # появляется сразу
            ("Continue", 280, 0.2),     # задержка 0.2 сек
            ("Settings", 360, 0.4),     # задержка 0.4 сек
            ("Exit", 440, 0.6),         # задержка 0.6 сек
        ]
        
        for text, y, delay in buttons_data:
            button = Button(400, y, button_img, 1, text, font)
            button.alpha = 0  # Начинаем с прозрачного
            button.visible = False
            
            # Сохраняем задержку как атрибут
            button.appear_delay = delay
            button.appear_timer = 0
            
            self.add_ui(button, group="menu")
    
    def on_enter(self):
        """Запускаем анимацию появления"""
        for element in self.ui_manager.get_group("menu"):
            element.visible = False
            element.alpha = 0
            element.appear_timer = 0
    
    def update(self, dt):
        """Обновляем анимацию"""
        super().update(dt)
        
        # Для каждой кнопки проверяем не пора ли появиться
        for element in self.ui_manager.get_group("menu"):
            if not element.visible:
                element.appear_timer += dt
                
                # Если прошло достаточно времени — показываем
                if element.appear_timer >= element.appear_delay:
                    element.show()  # Плавное появление через alpha
    
    def render(self, screen):
        screen.fill(WHITE)
        super().render(screen)


# ============================================================================
# ПРИМЕР 5: Диалоговое окно поверх другой сцены
# ============================================================================

class DialogScene(Scene):
    """Диалоговое окно с подтверждением"""
    
    def __init__(self, director, message="Are you sure?", on_confirm=None):
        super().__init__(director)
        self.message = message
        self.on_confirm = on_confirm
        self._setup_ui()
    
    def _setup_ui(self):
        font_title = self.resource_manager.get_font("main", 24)
        font_button = self.resource_manager.get_font("main", 20)
        button_img = self.resource_manager.get_image("button")
        
        # Текст сообщения
        self.text = Text(400, 250, self.message, font_title)
        
        # Кнопки Да/Нет
        self.btn_yes = Button(300, 350, button_img, 1, "Yes", font_button)
        self.btn_no = Button(500, 350, button_img, 1, "No", font_button)
        
        self.btn_yes.on_click = self._on_yes
        self.btn_no.on_click = self._on_no
        
        # Добавляем в UI
        self.add_ui(self.text)
        self.add_ui(self.btn_yes)
        self.add_ui(self.btn_no)
    
    def _on_yes(self, button):
        if self.on_confirm:
            self.on_confirm()
        self.director.switch_scene("menu")
    
    def _on_no(self, button):
        self.director.switch_scene("menu")
    
    def render(self, screen):
        # Полупрозрачный фон
        overlay = pg.Surface((800, 700))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        screen.blit(overlay, (0, 0))
        
        # Белый прямоугольник для диалога
        dialog_rect = pg.Rect(200, 150, 400, 300)
        pg.draw.rect(screen, WHITE, dialog_rect)
        pg.draw.rect(screen, BLACK, dialog_rect, 3)
        
        # UI элементы
        super().render(screen)


# ============================================================================
# ПРИМЕР 6: Использование в director.py
# ============================================================================

"""
# В director.py добавьте регистрацию новых сцен:

def _register_scenes(self):
    from Scenes import MenuScene, CreationScene, InfoBoxScene
    from examples import SimpleScene, AdvancedMenuScene, RegistrationScene
    
    self.scenes = {
        "menu": MenuScene(self),
        "creation": CreationScene(self),
        "infobox": InfoBoxScene(self),
        
        # Новые сцены из примеров
        "simple": SimpleScene(self),
        "advanced_menu": AdvancedMenuScene(self),
        "registration": RegistrationScene(self),
    }
"""


# ============================================================================
# ПРИМЕР 7: Горячие клавиши
# ============================================================================

class HotkeysScene(Scene):
    """Демонстрация горячих клавиш"""
    
    def __init__(self, director):
        super().__init__(director)
        self._setup_ui()
    
    def _setup_ui(self):
        font = self.resource_manager.get_font("main", 20)
        button_img = self.resource_manager.get_image("button")
        
        # Кнопки с подсказками о горячих клавишах
        self.btn_play = Button(400, 200, button_img, 1, "Play (P)", font)
        self.btn_settings = Button(400, 280, button_img, 1, "Settings (S)", font)
        self.btn_quit = Button(400, 360, button_img, 1, "Quit (Q)", font)
        
        # Сохраняем горячие клавиши
        self.hotkeys = {
            pg.K_p: self.btn_play,
            pg.K_s: self.btn_settings,
            pg.K_q: self.btn_quit,
        }
        
        self.add_ui(self.btn_play)
        self.add_ui(self.btn_settings)
        self.add_ui(self.btn_quit)
    
    def handle_events(self, events):
        """Обрабатываем горячие клавиши"""
        for event in events:
            if event.type == pg.KEYDOWN:
                # Проверяем есть ли горячая клавиша
                if event.key in self.hotkeys:
                    button = self.hotkeys[event.key]
                    # Имитируем нажатие кнопки
                    if button.on_click:
                        button.on_click(button)
        
        super().handle_events(events)
    
    def render(self, screen):
        screen.fill(WHITE)
        super().render(screen)