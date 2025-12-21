from typing import Dict, Any, Optional, List
from cat.cat import Cat

class MC_Cat(Cat):
    def __init__(
            self,
            cat_id: Optional[int] = None, #Эта запись значит что может быть либо int либо None
            postfix: str = "",
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
            kits_ids: Optional[List[int]] = None,
            skills: Optional[Dict[str, int]] = None
        ):
        super().__init__(
            cat_id=cat_id,
            postfix=postfix,
            age=age,
            alive=alive,
            alliance=alliance,
            rank=rank,
            social_opinion=social_opinion,
            pelt=pelt,
            color=color,
            eyes=eyes,
            first_trait=first_trait,
            second_trait=second_trait,
            first_skill=first_skill,
            second_skill=second_skill,
            parents_ids=parents_ids,
            kits_ids=kits_ids
        )
        if skills is None:
            self.skills = {
                "hunting": 0,   # охота
                "fighting": 0,  # бой
                "healing": 0,   # лечение
                "stealth": 0,   # скрытность
            }
        else:
            self.skills = skills

    def improve_skill(self, skill_name: str, amount: int = 1):
        """
        Улучшить конкретный навык
        
        Args:
            skill_name: название навыка
            amount: на сколько улучшить
        """
        if skill_name in self.skills:
            self.skills[skill_name] += amount
            return self.skills[skill_name]
        else:
            raise ValueError(f"Неизвестный навык: {skill_name}")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразовать в словарь для сохранения
        
        Расширяет базовый метод дополнительными полями
        """
        data = super().to_dict()
        
        # Добавляем специфичные для игрока поля
        data.update({
            "skills": self.skills
        })
        
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MC_Cat':
        """
        Создать из словаря (загрузка)
        
        Args:
            data: словарь с данными
            
        Returns:
            Экземпляр MC_Cat
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
            kits_ids=data.get("kits_ids"),
            skills=data.get("skills")
        )
    
    def get_description(self) -> str:
        """
        Получить описание с дополнительной информацией
        
        Returns:
            Расширенное описание игрока
        """
        desc = super().get_description()
        
        # Добавляем информацию об уровне и навыках
        desc += f"\n  Навыки:"
        for skill, value in self.skills.items():
            desc += f"\n    • {skill}: {value}"
        
        return desc