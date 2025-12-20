import pygame as pg
from Scenes.scene import Scene
from config import BEIGE, BROWN
from tools.text import Text
from tools.input_box import Input_box
from tools.button import Button

class CreationScene(Scene):
    """
    Сцена создания персонажа
    
    Демонстрирует:
    - Работу с Input_box (поле ввода)
    - Группировку UI элементов
    - Callback функции для обработки ввода
    """
    
    def __init__(self, director):
        super().__init__(director)
        
        # Загружаем изображения
        self.bg_img = self.resource_manager.get_image("clan_four_light")
        self.bg_rect = self.bg_img.get_rect() if self.bg_img else None
        
        self.frame_img_bg = self.resource_manager.get_image("basic_frame")
        self.frame_bg_rect = self.frame_img_bg.get_rect() if self.frame_img_bg else None
        
        # Создаём UI
        self._setup_ui()
    
    def _setup_ui(self):
        """Настройка UI элементов"""
        font_main = self.resource_manager.get_font("main", 15)
        font_button = self.resource_manager.get_font("main", 20)
        
        # === Текстовые поля ===
        self.title = Text(
            400, 180, 
            "StarClan is looking down upon you...", 
            font_main,
            text_color=BROWN
        )
        
        self.title2 = Text(
            400, 230, 
            "What is your name?", 
            font_main,
            text_color=BROWN
        )
        
        self.suffix_label = Text(
            510, 290, 
            "-kit",  # Суффикс имени котёнка
            font_main,
            text_color=BROWN
        )
        
        # Добавляем текстовые элементы в группу "labels"
        self.add_ui(self.title, group="labels")
        self.add_ui(self.title2, group="labels")
        self.add_ui(self.suffix_label, group="labels")
        
        # === Поле ввода ===
        frame_img = self.resource_manager.get_image("clan_name_frame")
        self.input_box = Input_box(
            frame_img, 370, 290, 
            font_main,
            text_color=BROWN,
            max_length=20  # Максимум 20 символов
        )
        
        # Устанавливаем callback для обработки ввода
        # Callback — это функция которая вызовется при определённом событии
        self.input_box.on_submit = self._on_name_submit
        self.input_box.on_text_change = self._on_text_change
        
        self.add_ui(self.input_box, group="input")
        
        # === Кнопки ===
        bt_img = self.resource_manager.get_image("clan_name_frame")
        bt_back = self.resource_manager.get_image("arr_l")
        bt_continue = self.resource_manager.get_image("arr_r")
        
        # Кнопка "Назад"
        self.bt_back = Button(50, 600, bt_back, 1, "", font_button, center=False)
        self.add_ui(self.bt_back, group="buttons")
        
        # Кнопка "Продолжить" (появится только когда имя введено)
        self.bt_continue = Button(650, 600, bt_continue, 1, "", font_button, center=False)
        self.bt_continue.enabled = False  # Изначально неактивна
        self.add_ui(self.bt_continue, group="buttons")
    
    def _on_name_submit(self, input_box, text):
        """
        Вызывается когда игрок нажимает Enter в поле ввода
        
        Args:
            input_box: сам элемент Input_box
            text: введённый текст
        """
        if text.strip():  # Проверяем что текст не пустой
            print(f"✓ Имя введено: {text}kit")
            # Переходим на следующую сцену
            # self.director.switch_scene("next_scene", player_name=text)
    
    def _on_text_change(self, input_box, text):
        """
        Вызывается каждый раз когда текст в поле меняется
        Используем для активации/деактивации кнопки "Продолжить"
        
        Args:
            input_box: сам элемент Input_box
            text: текущий текст
        """
        # Активируем кнопку только если введено хотя бы 2 символа
        if len(text.strip()) >= 2:
            self.bt_continue.enabled = True
        else:
            self.bt_continue.enabled = False
    
    def on_enter(self):
        """Вызывается при входе в сцену"""
        print("→ Вход в сцену создания персонажа")
        
        # Автоматически ставим фокус на поле ввода
        # Теперь игрок может сразу начать печатать
        self.input_box.focus()
        
        # Показываем все элементы
        self.show_group("labels")
        self.show_group("input")
        self.show_group("buttons")
    
    def on_exit(self):
        """Вызывается при выходе из сцены"""
        print("← Выход из сцены создания")
        # Очищаем поле ввода для следующего раза
        self.input_box.clear()
    
    def handle_events(self, events):
        """Обработка событий"""
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    # ESC — возврат в меню
                    self.director.switch_scene("menu")
        
        # Передаём события в UI Manager
        # Он сам передаст их в input_box для обработки текста
        super().handle_events(events)
    
    def update(self, dt):
        """Обновление логики"""
        super().update(dt)
        
        # Здесь можно добавить анимации или другую логику
    
    def render(self, screen):
        """Отрисовка сцены"""
        # 1. Фон
        screen.fill(BEIGE)
        
        # 2. Рисуем рамки снизу экрана
        if self.frame_img_bg and self.frame_bg_rect:
            self.frame_bg_rect.bottom = screen.get_height()
            screen.blit(self.frame_img_bg, self.frame_bg_rect)
        
        if self.bg_img and self.bg_rect:
            self.bg_rect.bottom = screen.get_height()
            screen.blit(self.bg_img, self.bg_rect)
        
        # 3. Проверяем нажатия кнопок и рисуем их
        if self.bt_back.draw(screen):
            self.director.switch_scene("menu")
        
        if self.bt_continue.draw(screen) and self.bt_continue.enabled:
            # Получаем введённое имя
            name = self.input_box.get_text()
            print(f"→ Продолжаем с именем: {name}-kit")
            # Здесь переход на следующую сцену
            # self.director.switch_scene("next_scene", player_name=name)
        
        # 4. Рисуем все UI элементы
        super().render(screen)