"""
Базовый класс для всех котов в игре

Этот класс определяет общие характеристики для всех котов:
- Внешность (окрас, цвет, глаза)
- Родственные связи (родители, котята)
- Уникальная идентификация (ID)
"""

import random
import json
from tools.chance import chance
from pathlib import Path
from typing import List, Optional, Dict, Any

class Cat:
    """
    Базовый класс кота
    
    Все коты в игре наследуются от этого класса
    Содержит общую логику для внешности и родственных связей
    """
    
    # Возможные значения для генерации котов
    PELT_TYPES = [
        "tabby",      # полосатый
        "solid",      # однотонный
        "tortie",     # черепаховый
        "calico",     # калико (трёхцветный)
        "spotted",    # пятнистый
        "tuxedo",     # смокинг (чёрно-белый)
    ]
    
    COLORS = [
        "brown",      # коричневый
        "black",      # чёрный
        "white",      # белый
        "orange",     # оранжевый
        "gray",       # серый
        "cream",      # кремовый
    ]
    
    EYE_COLORS = [
        "yellow",     # жёлтый
        "green",      # зелёный
        "blue",       # голубой
        "amber",      # янтарный
        "copper",     # медный
    ]

    TRAITS_1 = [
        "Brave",
        "Loyal",
        "Compassionate",
        "Patient",
        "Protective",
        "Honest",
        "Calm",
        "Determined",
        "Gentle",
        "Observant",
    ]

    TRAITS_2 = [
        "Aggressive",
        "Arrogant",
        "Jealous",
        "Impulsive",
        "Cowardly",
        "Manipulative",
        "Cold-hearted",
        "Stubborn",
        "Blood-thirsty",
        "Cruel",
    ]

    SKILLS_1 = [
        "Good hunter",
        "Fast runner",
        "Strong swimmer",
        "Knows forest paths well",
        "Climbs trees easily",
        "Silent walker",
        "Good night vision",
        "Endures cold well",
        "Quick learner",
        "Strong sense of smell",
    ]

    SKILLS_2 = [
        "Connection to Starclan",
        "Connection to Dark Forest",
        "Sees things others cannot see",
        "Prophesying"
    ]
    
    # Счётчик для генерации уникальных ID
    _next_id = 1
    
    def __init__(
        self,
        cat_id: Optional[int] = None, #Эта запись значит что может быть либо int либо None
        postfix: str = "",
        suffix: str = "",
        name: str = "",
        age: Optional[int] = None,
        alive: Optional[bool] = None,
        alliance: Optional[str] = None,
        rank: Optional[str] = None,
        social_opinion: Optional[int] = None,
        pelt: Optional[str] = None,
        color: Optional[str] = None,
        eyes: Optional[str] = None,
        first_trait: Optional[str] = None,
        second_trait: Optional[str] = None,
        first_skill: Optional[str] = None,
        second_skill: Optional[str] = None,
        parents_ids: Optional[List[int]] = None,
        kits_ids: Optional[List[int]] = None
    ):
        if cat_id is None:
            self.id = Cat._next_id
            Cat._next_id += 1
        else:
            self.id = cat_id
            if cat_id >= Cat._next_id:
                Cat._next_id = cat_id + 1
        
        # СНАЧАЛА базовые атрибуты
        self.age = age if age else random.randint(0, 180)
        self.alive = alive if alive else True
        
        # ПОТОМ методы, которые их используют
        self.alliance = self.set_alliance(alliance)
        self.rank = self.set_rank(rank)
        
        # Остальное
        self.pelt = pelt if pelt else random.choice(Cat.PELT_TYPES)
        self.color = color if color else random.choice(Cat.COLORS)
        self.eyes = eyes if eyes else random.choice(Cat.EYE_COLORS)
        self.first_trait = first_trait if first_trait else random.choice(Cat.TRAITS_1)
        self.second_trait = second_trait if second_trait else random.choice(Cat.TRAITS_2)
        self.first_skill = first_skill if first_skill else random.choice(Cat.SKILLS_1)
        
        if second_skill:
            self.second_skill = second_skill 
        elif chance(15):
            self.second_skill = random.choice(Cat.SKILLS_2)
        else:
            self.second_skill = None  # Явно указать None
        
        self.social_opinion = social_opinion if social_opinion else random.randint(-100, 100)
        
        # Имя
        self.postfix = postfix
        self.suffix = suffix
        if "kitten" in self.rank:
            self.name = f"{postfix}kit"
        elif "apprentice" in self.rank:
            self.name = f"{postfix}paw"
        elif "leader" in self.rank:
            self.name = f"{postfix}Star"
        else:
            self.name = f"{postfix}{suffix}"
        
        # Родственные связи
        self.parents_ids = parents_ids if parents_ids else []
        self.kits_ids = kits_ids if kits_ids else []
    
    def add_kit(self, kit_id: int):
        """
        Добавить котёнка в список детей
        
        Args:
            kit_id: ID котёнка
        """
        if kit_id not in self.kits_ids:
            self.kits_ids.append(kit_id)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразовать кота в словарь для сохранения в JSON
        
        Returns:
            Словарь с данными кота
        """
        data = {
                "id": self.id,
                "type": self.__class__.__name__, 
                "postfix": self.postfix,
                "suffix": self.suffix,
                "name": self.name,
                "age": self.age,
                "alive": self.alive,
                "alliance": self.alliance,
                "rank": self.rank,
                "social_opinion": self.social_opinion,
                "pelt": self.pelt,
                "color": self.color,
                "eyes": self.eyes,
                "first_trait": self.first_trait,
                "second_trait": self.second_trait,
                "first_skill": self.first_skill,
                "second_skill": self.second_skill,
                "parents_ids": self.parents_ids,
                "kits_ids": self.kits_ids
            }
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Cat':
        """
        Создать кота из словаря (загрузка из JSON)
        
        Args:
            data: словарь с данными кота
            
        Returns:
            Экземпляр кота
        """
        return cls(
            cat_id=data.get("id"),
            postfix=data.get("postfix"),
            suffix=data.get("suffix"),
            name=data.get("name"),
            age=data.get("age"),
            alive=data.get("alive"),
            alliance=data.get("alliance"),
            rank=data.get("rank"),
            social_opinion=data.get("social_opinion"),
            pelt=data.get("pelt"),
            color=data.get("color"),
            eyes=data.get("eyes"),
            first_trait=data.get("first_trait"),
            second_trait=data.get("second_trait"),
            first_skill=data.get("skill"),
            second_skill=data.get("second_skill"),
            parents_ids=data.get("parents_ids"),
            kits_ids=data.get("kits_ids")
        )
    
    def get_description(self) -> str:

        """ Получить текстовое описание кота Returns:
            Строка с описанием внешности """
    
        desc = f"{self.name} (ID: {self.id})"

        if self.age is not None:
            desc += f"\n  Age: {self.age}"

        if self.alive is not None:
            status = "Alive" if self.alive else "Dead"
            desc += f"\n  Status: {status}"

        if self.alliance:
            desc += f"\n  Alliance: {self.alliance}"

        if self.rank:
            desc += f"\n  Rank: {self.rank}"

        if self.pelt or self.color:
            desc += f"\n  Pelt: {self.pelt or 'Unknown'} {self.color or ''}".rstrip()

        if self.eyes:
            desc += f"\n  Eyes: {self.eyes}"

        if self.first_trait or self.second_trait:
            traits = [t for t in (self.first_trait, self.second_trait) if t]
            desc += f"\n  Traits: {', '.join(traits)}"

        if self.first_skill or self.second_skill:
            skills = [s for s in (self.first_skill, self.second_skill) if s]
            desc += f"\n  Skills: {', '.join(skills)}"

        if self.parents_ids:
            desc += f"\n  Parents: {', '.join(f'#{pid}' for pid in self.parents_ids)}"

        if self.kits_ids:
            desc += f"\n  Kits: {', '.join(f'#{kid}' for kid in self.kits_ids)}"

        return desc


    def __repr__(self) -> str:
        """Debug representation"""
        return (
            f"<{self.__class__.__name__} "
            f"id={self.id} "
            f"name='{self.name}' "
            f"alive={self.alive}>"
        )


    def __str__(self) -> str:
        """Human-readable string representation"""
        return self.get_description()

    
    def set_alliance(self, alliance=None):
        if self.alive == True:
            if alliance not in ["CLAN", "LONER", "KITTYPET"]:
                return random.choice(["CLAN", "LONER", "KITTYPET"])
            else:
                return alliance
        elif self.alive == False:
            if alliance not in ["SC", "DF", "UR"]:
                return random.choice(["SC", "DF", "UR"])
            return alliance
        else: 
            raise ValueError(f"Invalid alive status: {self.alive}. Must be True or False")
        

    def set_rank(self, rank = None):
        if self.alliance == "CLAN" or self.alliance == "LONER" or self.alliance == "KITTYPET":
            if self.age <= 5:
                return "kitten"
            elif self.alliance == "LONER":
                return "loner"
            elif self.alliance == "KITTYPET":
                return "kittypet"
            elif self.alliance == "CLAN":
                if self.age <= 11:
                    return "apprentice"
                elif self.age <= 119:
                    if rank == None:
                        return "warrior"
                    elif rank == "leader":
                        return "leader"
                    elif rank == "deputy":
                        return "deputy"
                    elif rank == "queen":
                        return "queen"
                else:
                    return "elder"
                
        if self.alliance == "UR":
            if self.age <= 5:
                return "ghost kitten"
            else:
                return "ghost"
            
        if self.alliance == "SC":
            if self.age <= 5:
                return "starclan kitten"
            if self.age <= 11:
                return "starclan apprentice"
            elif self.age <= 119:
                if rank == None:
                    return "starclan warrior"
                elif rank == "leader":
                    return "starclan leader"
                elif rank == "deputy":
                    return "starclan deputy"
                elif rank == "queen":
                    return "starclan queen"
                else:
                    return "starclan elder"
        if self.alliance == "DF":
            if self.age <= 5:
                return "dark forest kitten"
            if self.age <= 11:
                return "dark forest apprentice"
            elif self.age <= 119:
                if rank == None:
                    return "dark forest warrior"
                elif rank == "leader":
                    return "dark forest leader"
                elif rank == "deputy":
                    return "dark forest deputy"
                elif rank == "queen":
                    return "dark forest queen"
                else:
                    return "dark forest elder"