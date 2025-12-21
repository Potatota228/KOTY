from typing import Dict, Any, Optional, List
from cat.cat import Cat
class NPC_Cat(Cat):
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
            kits_ids: Optional[List[int]] = None,
            relationship: int = 0 #Отношение к гг
            #Потом как то добавлять отношения между всеми котами? Нужно ли это делать? Система в clangen слишком сложная, надо упрощать 
        ):
        super().__init__(
            cat_id=cat_id,
            postfix=postfix,
            suffix=suffix,
            name=name,
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
        self.relationship = 0


    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразовать в словарь для сохранения
        
        Расширяет базовый метод дополнительными полями
        """
        data = super().to_dict()
        
        # Добавляем специфичные для NPC поля
        data.update({
            "status": self.status,
            "personality": self.personality,
            "relationship": self.relationship
        })
        
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'NPC_Cat':
        """
        Создать из словаря (загрузка)
        
        Args:
            data: словарь с данными
            
        Returns:
            Экземпляр NPC_Cat
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
            relationship=data.get("relationship", 0)
        )
    

    #Добавить изменения относительно родственных связей
    def change_relationship_with_mc(self, amount):
        self.relationship += amount

    def get_relationship_status_with_mc(self):
        if self.relationship >= 75:
            return "близкий друг"
        elif self.relationship >= 50:
            return "друг"
        elif self.relationship >= 25:
            return "приятель"
        elif self.relationship >= -25:
            return "нейтральный"
        elif self.relationship >= -50:
            return "недолюбливает"
        elif self.relationship >= -75:
            return "враждебный"
        else:
            return "заклятый враг"