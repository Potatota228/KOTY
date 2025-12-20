import pygame as pg
from Scenes.scene import Scene
from config import BLUE
from tools.button import Button

class MenuScene(Scene):
    """
    Главное меню игры
    
    Демонстрирует использование UIManager для управления кнопками
    """
    
    def __init__(self, director):
        super().__init__(director)
        
        # Фоновое изображение (загружаем сразу)
        self.bg_image = self.resource_manager.get_image("menu_bg")
        self.bg_rect = self.bg_image.get_rect() if self.bg_image else None
        
        # Создаём UI элементы
        self._setup_ui()
    
    def _setup_ui(self):
        """
        Настройка всех UI элементов сцены
        Вызывается один раз при создании сцены
        """
        # Получаем шрифт и изображение кнопки из ресурсов
        font = self.resource_manager.get_font("main", 20)
        bt_img = self.resource_manager.get_image("button")
        
        # Создаём кнопки
        # center=False означает что x,y — это верхний левый угол
        self.bt_start = Button(50, 400, bt_img, 1, "Start", font, center=False)
        self.bt_infobox = Button(50, 500, bt_img, 1, "Info", font, center=False)
        
        # Добавляем кнопки в UI Manager в группу "main_menu"
        # Группы позволяют управлять несколькими элементами сразу
        self.add_ui(self.bt_start, group="main_menu")
        self.add_ui(self.bt_infobox, group="main_menu")
    
    def on_enter(self):
        """
        Вызывается при входе в сцену
        Здесь можно запустить музыку, показать элементы с анимацией и т.д.
        """
        print("→ Вход в главное меню")
        
        # Показываем все кнопки меню
        self.show_group("main_menu")
        
        # Можно добавить фоновую музыку
        # bg_music = self.resource_manager.get_sound("background_music")
        # if bg_music:
        #     pg.mixer.music.load(...)
        #     pg.mixer.music.play(-1)  # -1 означает зациклить
    
    def on_exit(self):
        """Вызывается при выходе из сцены"""
        print("← Выход из главного меню")
    
    def handle_events(self, events):
        """
        Обработка событий
        Сначала обрабатываем клавиатуру, потом передаём в UI Manager
        """
        for event in events:
            # Обработка горячих клавиш
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    # Пробел — быстрый старт
                    self.director.switch_scene("creation")
                elif event.key == pg.K_ESCAPE:
                    # ESC — выход из игры
                    self.director.quit()
        
        # Передаём события в UI Manager (он обработает клики на кнопках)
        super().handle_events(events)
    
    def update(self, dt):
        """
        Обновление логики меню
        dt — время с прошлого кадра (для анимаций)
        """
        # Обновляем UI элементы (анимации, состояния)
        super().update(dt)
        
        # Проверяем нажатия кнопок через их метод draw
        # (это унаследованное поведение от старого кода)
    
    def render(self, screen):
        """
        Отрисовка меню
        Порядок важен: сначала фон, потом элементы, потом UI
        """
        # 1. Заливаем экран цветом (на случай если фон не загрузился)
        screen.fill(BLUE)
        
        # 2. Рисуем фоновое изображение
        if self.bg_image and self.bg_rect:
            screen.blit(self.bg_image, self.bg_rect)
        
        # 3. Проверяем нажатия кнопок И рисуем их
        # ВАЖНО: draw() возвращает True если кнопка была нажата
        if self.bt_start.draw(screen):
            self.director.switch_scene("creation")
        
        if self.bt_infobox.draw(screen):
            self.director.switch_scene("infobox")
        
        # 4. Рисуем остальные UI элементы через менеджер
        # (в данном случае кнопки уже нарисованы выше, но для других элементов это важно)
        super().render(screen)