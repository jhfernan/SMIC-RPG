from math import ceil
from random import randint


class Character:

    def __init__(self, **kwargs):
        self.level = kwargs.get('level') if kwargs.get('level') else 1
        self.name = kwargs.get('name') or 'character'
        self.health = ceil(kwargs.get('health') * self.level) if kwargs.get('health') else 7
        self.current_health = self.health
        self.attack = ceil(kwargs.get('attack') * self.level) if kwargs.get('attack') else 4
        self.current_attack = self.attack
        self.defense = ceil(kwargs.get('defense') * self.level) if kwargs.get('defense') else 0
        self.current_defense = self.defense

    def attack_one(self):
        total = self.current_attack
        result = f"The {self.name} uses their basic attack"
        if self.attack_roll() > 85:
            result += " It is a critical hit!!!"
            return total * 2
        result += f"\nThe attack causes {total} damage"
        return self.result_string(result, total)

    def attack_two(self):
        result = f"The {self.name} gains focus and increases their attack!"
        self.current_attack = ceil(self.current_attack * 1.5)
        return self.result_string(result, 0)

    def attack_three(self):
        total = self.current_attack * 2
        result = f"The {self.name} uses their ultimate attack for {total} damage"
        return self.result_string(result, 0)

    def gets_hit(self, damage):
        total = damage - self.defense
        if total < 0:
            total = 0
        elif total > 0 and self.attack_roll() > 95:
            print("The attack missed!")
            total = 0
        print(f"The {self.name} takes {total} damage")
        self.current_health -= total

    @staticmethod
    def attack_roll():
        return randint(1, 100)

    @staticmethod
    def result_string(results, total):
        print(results)
        return total


class Monster(Character):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.turn = 0

    def attack_choice(self):
        attack_number = self.turn % 3
        self.turn += 1
        if attack_number == 0:
            return self.attack_one()
        elif attack_number == 1:
            return self.attack_two()
        elif attack_number == 2:
            return self.attack_three()


class Player(Character):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.spirit = kwargs.get('spirit') or 4
        self.spirit_current = 0
        self.spirit_regen = kwargs.get('spirit_regen') or 2
        self.experience = 0
        self.attack_two_requirement = kwargs.get('attack_two_requirement') or 2
        self.attack_three_requirement = kwargs.get('attack_three_requirement') or 3

    def refresh_spirit(self):
        print(f"The player regenerates {self.spirit_regen} spirit points")
        self.spirit_current += self.spirit_regen
        if self.spirit_current > self.spirit:
            self.spirit_current = self.spirit

    def attack_one(self):
        total = super().attack_one()
        self.refresh_spirit()
        return total