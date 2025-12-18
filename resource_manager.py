import pygame as pg
from pathlib import Path

class ResourceManager:
    """Централизованное управление ресурсами игры"""
    
    def __init__(self):
        self.images = {}
        self.fonts = {}
        self.sounds = {}
        
    def load_image(self, key, path, convert_alpha=True, colorkey=None):
        """Загрузка и кэширование изображений"""
        if key not in self.images:
            try:
                img = pg.image.load(path)
                if convert_alpha:
                    img = img.convert_alpha()
                if colorkey:
                    img.set_colorkey(colorkey)
                self.images[key] = img
                print(f"✓ Загружено изображение: {key}")
            except Exception as e:
                print(f"✗ Ошибка загрузки {path}: {e}")
                # Создаём заглушку
                self.images[key] = self._create_placeholder(100, 100)
        return self.images[key]
    
    def load_font(self, key, path, size):
        """Загрузка и кэширование шрифтов"""
        font_key = f"{key}_{size}"
        if font_key not in self.fonts:
            try:
                self.fonts[font_key] = pg.font.Font(path, size)
            except Exception as e:
                print(f"✗ Ошибка загрузки шрифта {path}: {e}")
                self.fonts[font_key] = pg.font.Font(None, size)
        return self.fonts[font_key]
    
    def get_image(self, key):
        """Получить загруженное изображение"""
        return self.images.get(key)
    
    def get_font(self, key, size):
        """Получить загруженный шрифт"""
        return self.fonts.get(f"{key}_{size}")
    
    def _create_placeholder(self, width, height):
        """Создать заглушку для отсутствующего изображения"""
        surf = pg.Surface((width, height))
        surf.fill((255, 0, 255))  # Розовый цвет для заметности
        return surf
    
    def preload_game_resources(self):
        """Предзагрузка всех ресурсов игры"""
        # Изображения
        self.load_image("menu_bg", "./images/menu.png")
        self.load_image("button", "./images/buttons/button.png")
        self.load_image("clan_four_light", "./images/clan_four_light.png")
        self.load_image("clan_name_frame", "./images/clan_name_frame.png")
        
        # Шрифты
        self.load_font("main", "HUDSonicX1-Regular.otf", 20)
        self.load_font("main", "HUDSonicX1-Regular.otf", 24)
        self.load_font("main", "HUDSonicX1-Regular.otf", 16)
    
    def clear(self):
        """Очистка всех ресурсов"""
        self.images.clear()
        self.fonts.clear()
        self.sounds.clear()