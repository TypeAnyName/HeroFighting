from __future__ import annotations
from abc import ABC, abstractmethod
from app.assets.equipment import Weapon, Armor
from app.assets.classes import UnitClass
from typing import Optional


class BaseUnit(ABC):
    """
    Базовый класс юнита
    """

    def __init__(self, name: str, unit_class: UnitClass, weapon, armor):
        """
        При инициализации класса Unit используем свойства класса UnitClass
        """
        self.name = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon = weapon
        self.armor = armor
        self._is_skill_used = False

    @property
    def health_points(self):
        return round(self.hp, 2)

    @property
    def stamina_points(self):
        return round(self.stamina)

    def equip_weapon(self, weapon: Weapon):
        self.weapon = weapon
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor):
        self.armor = armor
        return f"{self.name} экипирован броней {self.armor.name}"

    def _count_damage(self, target: BaseUnit):
        counting_damage = self.weapon.damage * self.unit_class.attack
        if target.stamina >= self.armor.stamina_per_turn:
            counting_armor = self.armor.defence * self.unit_class.armor
        else:
            counting_armor = 0
        damage = counting_damage - counting_armor
        self.stamina -= self.weapon.stamina_per_hit
        target.get_damage(damage)
        return damage

    def get_damage(self, damage: float):
        self.hp -= damage

    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        pass

    def use_skill(self, target: BaseUnit) -> str:
        if self._is_skill_used:
            result = "Умение уже использовано"
            return result
        else:
            self.unit_class.skill.use(user=self, target=target)
            self._is_skill_used = True
            result = f"{self.name} использует {self.unit_class.skill.name} и наносит {round(self.unit_class.skill.damage, 2)} урона сопернику."
            return result


class PlayerUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        if self.stamina >= self.weapon.stamina_per_hit:
            damage = self._count_damage(target)
            if damage <= 0:
                result = f"{self.name} используя {self.weapon.name} наносит удар, но {target.armor.name} cоперника его останавливает."
                return result
            elif damage > 0:
                result = f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит {round(damage, 2)} урона."
                return result
        else:
            result = f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."
            return result


class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        if self._is_skill_used:
            if self.stamina >= self.weapon.stamina_per_hit:
                damage = self._count_damage(target)
                if damage <= 0:
                    result = f"{self.name} используя {self.weapon.name} наносит удар, но {target.armor.name} cоперника его останавливает."
                    return result
                elif damage > 0:
                    result = f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит {round(damage, 2)} урона."
                    return result
            else:

                result = f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."
                return result
        else:
            result = self.use_skill(target)
            return result
