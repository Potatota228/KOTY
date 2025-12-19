import pygame as pg
from Scenes.scene import Scene
from config import BEIGE, BROWN
from tools.text import Text
from tools.input_box import Input_box

class CreationScene(Scene):
    """Сцена создания клана"""
    
    def __init__(self, director):
        super().__init__(director)
        self._setup_ui()
    
    def _setup_ui(self):
        """Настройка UI элементов"""
        # Загружаем изображения из менеджера ресурсов
        self.bg_img = self.resource_manager.get_image("clan_four_light")
        self.bg_rect = self.bg_img.get_rect() if self.bg_img else None
        
        self.frame_img_bg = self.resource_manager.get_image("basic_frame")
        self.frame_bg_rect = self.frame_img_bg.get_rect() if self.frame_img_bg else None
        
        # Получаем шрифт
        font = self.resource_manager.get_font("main", 15)
        
        # Создаём текстовые поля
        self.title = Text(
            400, 180, 
            "StarClan is looking down upon you...", 
            font,
            text_color=BROWN
        )
        self.title2 = Text(
            400, 230, 
            "What is your name?", 
            font,
            text_color=BROWN
        )

        self.title3 = Text(
            510, 290, 
            "-kit", 
            font,
            text_color=BROWN
        )
        
        # Создаём поле ввода
        f_img = self.resource_manager.get_image("clan_name_frame")
        self.input_box = Input_box(
            f_img, 370, 290, 
            font,
            text_color=BROWN,
            max_length=20
        )
        
        # Callback при отправке (Enter)
        def on_name_submit(inp, text):
            if text:
                print(f"Имя введено: {text}")
                # Здесь можно перейти на следующий экран
                # self.director.switch_scene("next_scene")
        
        self.input_box.on_submit = on_name_submit
    
    def on_enter(self):
        """Вызывается при входе в сцену"""
        print("Вход в сцену создания")
        # Автоматически ставим фокус на поле ввода
        self.input_box.focus()
    
    def handle_events(self, events):
        """Обработка событий"""
        for event in events:
            # Передаём события в input_box!
            self.input_box.handle_event(event)
            
            # Обработка клавиш
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.director.switch_scene("menu")
    
    def update(self, dt):
        """Обновление логики"""
        self.input_box.update(dt)
    
    def render(self, screen):
        """Отрисовка сцены"""
        screen.fill(BEIGE)
        
        # Рисуем фоновую рамку
        if self.frame_img_bg and self.frame_bg_rect:
            self.frame_bg_rect.bottom = screen.get_height()
            screen.blit(self.frame_img_bg, self.frame_bg_rect)
        
        # Рисуем фон снизу
        if self.bg_img and self.bg_rect:
            self.bg_rect.bottom = screen.get_height()
            screen.blit(self.bg_img, self.bg_rect)
        
        # Рисуем текстовые поля
        self.title.draw(screen)
        self.title2.draw(screen)
        self.title3.draw(screen)
        
        # Рисуем поле ввода
        self.input_box.draw(screen)