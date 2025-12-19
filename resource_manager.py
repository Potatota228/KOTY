import pygame as pg
import json
from pathlib import Path

class ResourceManager:
    """Централизованное управление ресурсами игры с загрузкой из конфига"""
    
    def __init__(self, config_path="resources.json"):
        self.images = {}
        self.fonts = {}
        self.sounds = {}
        self.config_path = config_path
        self.config = self._load_config()
        
    def _load_config(self):
        """Загрузка конфигурационного файла"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                print(f"✓ Конфигурация загружена из {self.config_path}")
                return config
        except FileNotFoundError:
            print(f"⚠ Файл {self.config_path} не найден, используются значения по умолчанию")
            return self._get_default_config()
        except json.JSONDecodeError as e:
            print(f"✗ Ошибка парсинга JSON: {e}")
            return self._get_default_config()
    
    def _get_default_config(self):
        """Конфигурация по умолчанию"""
        return {
            "images": {},
            "fonts": {},
            "sounds": {},
            "settings": {
                "image_placeholder_size": [100, 100],
                "image_placeholder_color": [255, 0, 255],
                "default_font_size": 20
            }
        }
    
    def load_image(self, key):
        """Загрузка и кэширование изображения по ключу из конфига"""
        if key in self.images:
            return self.images[key]
        
        # Проверяем наличие ключа в конфиге
        if key not in self.config.get("images", {}):
            print(f"✗ Ключ '{key}' не найден в images конфига")
            self.images[key] = self._create_placeholder()
            return self.images[key]
        
        # Получаем параметры из конфига
        img_config = self.config["images"][key]
        path = img_config.get("path")
        convert_alpha = img_config.get("convert_alpha", True)
        colorkey = img_config.get("colorkey")
        
        if colorkey:
            colorkey = tuple(colorkey)
        
        if not path:
            print(f"✗ Путь для изображения '{key}' не найден в конфиге")
            self.images[key] = self._create_placeholder()
            return self.images[key]
        
        try:
            img = pg.image.load(path)
            if convert_alpha:
                img = img.convert_alpha()
            if colorkey:
                img.set_colorkey(colorkey)
            self.images[key] = img
            print(f"✓ Загружено изображение: {key} ({path})")
        except Exception as e:
            print(f"✗ Ошибка загрузки {path}: {e}")
            self.images[key] = self._create_placeholder()
        
        return self.images[key]
    
    def load_font(self, key, size=None):
        """Загрузка и кэширование шрифта по ключу из конфига"""
        # Если размер не указан, берём из настроек
        if size is None:
            size = self.config.get("settings", {}).get("default_font_size", 20)
        
        font_key = f"{key}_{size}"
        
        if font_key in self.fonts:
            return self.fonts[font_key]
        
        # Проверяем наличие ключа в конфиге
        if key not in self.config.get("fonts", {}):
            print(f"✗ Ключ '{key}' не найден в fonts конфига")
            self.fonts[font_key] = pg.font.Font(None, size)
            return self.fonts[font_key]
        
        # Получаем параметры из конфига
        font_config = self.config["fonts"][key]
        path = font_config.get("path")
        
        if not path:
            print(f"✗ Путь для шрифта '{key}' не найден в конфиге")
            self.fonts[font_key] = pg.font.Font(None, size)
            return self.fonts[font_key]
        
        try:
            self.fonts[font_key] = pg.font.Font(path, size)
            print(f"✓ Загружен шрифт: {key} размер {size}")
        except Exception as e:
            print(f"✗ Ошибка загрузки шрифта {path}: {e}")
            self.fonts[font_key] = pg.font.Font(None, size)
        
        return self.fonts[font_key]
    
    def load_sound(self, key):
        """Загрузка и кэширование звука по ключу из конфига"""
        if key in self.sounds:
            return self.sounds[key]
        
        # Проверяем наличие ключа в конфиге
        if key not in self.config.get("sounds", {}):
            print(f"✗ Ключ '{key}' не найден в sounds конфига")
            self.sounds[key] = None
            return None
        
        # Получаем параметры из конфига
        sound_config = self.config["sounds"][key]
        path = sound_config.get("path")
        volume = sound_config.get("volume", 1.0)
        
        if not path:
            print(f"✗ Путь для звука '{key}' не найден в конфиге")
            self.sounds[key] = None
            return None
        
        try:
            sound = pg.mixer.Sound(path)
            if volume is not None:
                sound.set_volume(volume)
            self.sounds[key] = sound
            print(f"✓ Загружен звук: {key} ({path})")
        except Exception as e:
            print(f"✗ Ошибка загрузки звука {path}: {e}")
            self.sounds[key] = None
        
        return self.sounds[key]
    
    def get_image(self, key):
        """Получить загруженное изображение (загружает, если ещё не загружено)"""
        if key not in self.images:
            return self.load_image(key)
        return self.images[key]
    
    def get_font(self, key, size=None):
        """Получить загруженный шрифт (загружает, если ещё не загружен)"""
        if size is None:
            size = self.config.get("settings", {}).get("default_font_size", 20)
        
        font_key = f"{key}_{size}"
        if font_key not in self.fonts:
            return self.load_font(key, size)
        return self.fonts[font_key]
    
    def get_sound(self, key):
        """Получить загруженный звук (загружает, если ещё не загружен)"""
        if key not in self.sounds:
            return self.load_sound(key)
        return self.sounds[key]
    
    def _create_placeholder(self):
        """Создать заглушку для отсутствующего изображения"""
        settings = self.config.get("settings", {})
        size = settings.get("image_placeholder_size", [100, 100])
        color = settings.get("image_placeholder_color", [255, 0, 255])
        
        surf = pg.Surface(size)
        surf.fill(color)
        
        # Рисуем крестик для наглядности
        pg.draw.line(surf, (0, 0, 0), (0, 0), size, 3)
        pg.draw.line(surf, (0, 0, 0), (size[0], 0), (0, size[1]), 3)
        
        return surf
    
    def preload_all_resources(self):
        """Предзагрузка всех ресурсов из конфига"""
        print("\n=== Загрузка ресурсов ===")
        
        # Загружаем все изображения
        for img_key in self.config.get("images", {}).keys():
            self.load_image(img_key)
        
        # Загружаем все шрифты во всех размерах
        for font_key, font_config in self.config.get("fonts", {}).items():
            sizes = font_config.get("sizes", [20])
            for size in sizes:
                self.load_font(font_key, size=size)
        
        # Загружаем все звуки
        for sound_key in self.config.get("sounds", {}).keys():
            self.load_sound(sound_key)
        
        print("=== Загрузка завершена ===\n")
    
    def reload_config(self):
        """Перезагрузка конфигурации"""
        self.config = self._load_config()
        print("Конфигурация перезагружена")
    
    def clear(self):
        """Очистка всех ресурсов"""
        self.images.clear()
        self.fonts.clear()
        self.sounds.clear()
        print("Ресурсы очищены")