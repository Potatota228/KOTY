import pygame as pg
from Scenes.scene import Scene
from config import WHITE, BLACK
from tools.button import Button
from tools.text import Text

class InfoBoxScene(Scene):
    """
    Сцена с информацией о игре
    
    Простая сцена для демонстрации базовых возможностей
    """
    
    def __init__(self, director):
        super().__init__(director)
        self._setup_ui()
    
    def _setup_ui(self):
        """Настройка UI элементов"""
        font_title = self.resource_manager.get_font("main", 32)
        font_text = self.resource_manager.get_font("main", 20)
        font_button = self.resource_manager.get_font("main", 20)
        
        # === Заголовок ===
        self.title = Text(
            400, 100,
            "KOTY - Warrior Cats Game",
            font_title,
            text_color=BLACK
        )
        self.add_ui(self.title, group="info")
        
        # === Описание ===
        # Создаём несколько строк текста
        info_texts = [
            "Create your own warrior cat and join a clan!",
            "",
            "Controls:",
            "SPACE - Quick start",
            "ESC - Back to menu",
            "",
            "This is a demo version.",
        ]
        
        y_offset = 200
        for line in info_texts:
            text = Text(
                400, y_offset,
                line,
                font_text,
                text_color=BLACK
            )
            self.add_ui(text, group="info")
            y_offset += 35  # Расстояние между строками
        
        # === Кнопка возврата ===
        bt_img = self.resource_manager.get_image("button")
        self.bt_back = Button(50, 600, bt_img, 1, "Back", font_button, center=False)
        self.add_ui(self.bt_back, group="buttons")
    
    def on_enter(self):
        """Вызывается при входе в сцену"""
        print(" Вход в информационную сцену")
        
        # Показываем все элементы
        self.show_group("info")
        self.show_group("buttons")
    
    def on_exit(self):
        """Вызывается при выходе из сцены"""
        print(" Выход из информационной сцены")
    
    def handle_events(self, events):
        """Обработка событий"""
        for event in events:
            if event.type == pg.KEYDOWN:
                # Любая клавиша — возврат в меню
                if event.key == pg.K_SPACE or event.key == pg.K_ESCAPE:
                    self.director.switch_scene("menu")
        
        # Передаём события в UI Manager
        super().handle_events(events)
    
    def update(self, dt):
        """Обновление логики"""
        super().update(dt)
    
    def render(self, screen):
        """Отрисовка сцены"""
        # 1. Белый фон
        screen.fill(WHITE)
        
        # 2. Проверяем и рисуем кнопку
        if self.bt_back.draw(screen):
            self.director.switch_scene("menu")
        
        # 3. Рисуем все UI элементы
        super().render(screen)