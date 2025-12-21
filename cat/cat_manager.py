"""
Менеджер котов - управление всеми котами и сохранениями

Отвечает за:
- Создание и хранение всех котов
- Сохранение в JSON файлы
- Загрузку из JSON файлов
- Получение котов по ID
- Генерацию семейных связей
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Union
from cat.cat import Cat
from cat.mc_cat import MC_Cat
from cat.npc_cat import NPC_Cat

class CatManager:
    """
    Менеджер для управления всеми котами в игре
    
    Singleton паттерн - существует только один экземпляр менеджера
    """
    
    _instance = None
    
    def __new__(cls):
        """Реализация Singleton - только один экземпляр"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Инициализация менеджера"""
        # Избегаем повторной инициализации при Singleton
        if hasattr(self, '_initialized'):
            return
        
        self._initialized = True
        
        # Словарь всех котов {id: объект_кота}
        self.cats: Dict[int, Union[Cat, MC_Cat, NPC_Cat]] = {}
        
        # Путь к папке с сохранениями
        self.save_dir = Path("saves")
        self.save_dir.mkdir(exist_ok=True)
        
        # ID игрока (None если игрок ещё не создан)
        self.player_id: Optional[int] = None
        
        print("CatManager инициализирован")
    
    def create_cat(
        self,
        cat_type: str = "npc",
        **kwargs
    ) -> Union[Cat, MC_Cat, NPC_Cat]:
        """
        Создать нового кота
        
        Args:
            cat_type: тип кота ("player", "npc", "base")
            name: имя кота
            **kwargs: дополнительные параметры для конкретного типа
            
        Returns:
            Созданный кот
        """
        # Выбираем класс в зависимости от типа
        if cat_type == "player":
            cat = MC_Cat(**kwargs)
            self.player_id = cat.id
        elif cat_type == "npc":
            cat = NPC_Cat(**kwargs)
        
        # Добавляем в словарь
        self.cats[cat.id] = cat
        
        print(f"Создан {cat_type} кот (ID: {cat.id})")
        return cat
    
    
    def get_cat(self, cat_id: int) -> Optional[Union[Cat, MC_Cat, NPC_Cat]]:
        """
        Получить кота по ID
        
        Args:
            cat_id: ID кота
            
        Returns:
            Объект кота или None если не найден
        """
        return self.cats.get(cat_id)
    
    def get_all_cats(self) -> List[Union[Cat, MC_Cat, NPC_Cat]]:
        """
        Получить список всех котов
        
        Returns:
            Список всех котов
        """
        return list(self.cats.values())
    
    
    def save_all(self, filename: str = "cats_save.json"):
        """
        Сохранить всех котов в один JSON файл
        
        Args:
            filename: имя файла для сохранения
        """
        filepath = self.save_dir / filename
        
        # Преобразуем всех котов в словари
        cats_data = []
        for cat in self.cats.values():
            cats_data.append(cat.to_dict())
        
        # Дополнительная информация о сохранении
        save_data = {
            "version": "1.0",
            "player_id": self.player_id,
            "cats": cats_data
        }
        
        # Сохраняем в файл с красивым форматированием
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Сохранено {len(cats_data)} котов в {filepath}")
    
    def load_all(self, filename: str = "cats_save.json"):
        """
        Загрузить всех котов из JSON файла
        
        Args:
            filename: имя файла для загрузки
        """
        filepath = self.save_dir / filename
        
        if not filepath.exists():
            print(f"Файл {filepath} не найден")
            return
        
        # Очищаем текущих котов
        self.cats.clear()
        
        # Загружаем из файла
        with open(filepath, 'r', encoding='utf-8') as f:
            save_data = json.load(f)
        
        # Восстанавливаем ID игрока
        self.player_id = save_data.get("player_id")
        
        # Загружаем всех котов
        cats_data = save_data.get("cats", [])
        
        for cat_data in cats_data:
            # Определяем тип кота по полю "type"
            cat_type = cat_data.get("type", "Cat")
            
            if cat_type == "MC_Cat":
                cat = MC_Cat.from_dict(cat_data)
            elif cat_type == "NPC_Cat":
                cat = NPC_Cat.from_dict(cat_data)
            
            self.cats[cat.id] = cat
        
        print(f"Загружено {len(cats_data)} котов из {filepath}")
    
    def print_all_cats(self):
        """Вывести информацию о всех котах"""
        if not self.cats:
            print("Нет котов в базе данных")
            return
        
        print(f"\n=== Всего котов: {len(self.cats)} ===\n")
        
        # Сначала выводим игрока
        player = self.get_player()
        if player:
            print("ИГРОК:")
            print(player.get_description())
            print()
        
        # Потом NPC по статусам
        npcs = [cat for cat in self.cats.values() if isinstance(cat, NPC_Cat)]
        if npcs:
            print("NPC:")
            for npc in npcs:
                print(npc.get_description())
                print()
    
    def clear_all(self):
        """Очистить всех котов (для нового начала)"""
        self.cats.clear()
        self.player_id = None
        Cat._next_id = 1  # Сбрасываем счётчик ID
        print(" Все коты удалены")
    
    def get_family_tree(self, cat_id: int, depth: int = 2) -> str:
        """
        Получить семейное древо кота
        
        Args:
            cat_id: ID кота
            depth: глубина (сколько поколений показывать)
            
        Returns:
            Строка с семейным древом
        """
        cat = self.get_cat(cat_id)
        if not cat:
            return f"Кот с ID {cat_id} не найден"
        
        tree = f"Семейное древо {cat.name}:\n"
        tree += self._build_tree(cat, depth, prefix="")
        return tree
    
    def _build_tree(self, cat: Cat, depth: int, prefix: str) -> str:
        """Рекурсивно строить дерево"""
        if depth <= 0:
            return ""
        
        tree = f"{prefix}├─ {cat.name} (ID: {cat.id})\n"
        
        # Родители
        if cat.parent1_id:
            parent1 = self.get_cat(cat.parent1_id)
            if parent1:
                tree += self._build_tree(parent1, depth - 1, prefix + "│  ")
        
        if cat.parent2_id:
            parent2 = self.get_cat(cat.parent2_id)
            if parent2:
                tree += self._build_tree(parent2, depth - 1, prefix + "│  ")
        
        return tree