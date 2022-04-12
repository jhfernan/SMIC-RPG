from math import ceil
from random import randint


class Character:

    def __init__(self, **kwargs):
        self.level = kwargs.get('level') if kwargs.get('level') else 1
        self.name = kwargs.get('name') or 'character'
        self.health = self.set_stat(self.level, kwargs.get('health'), 7)
        self.current_health = self.health
        self.attack = self.set_stat(self.level, kwargs.get('attack'), 4)
        self.current_attack = self.attack
        self.defense = self.set_stat(self.level, kwargs.get('defense'), 0)
        self.current_defense = self.defense
        self.atk_one_name = kwargs.get('atk_one_name') if kwargs.get('atk_one_name') else "Basic Attack"
        self.atk_two_name = kwargs.get('atk_two_name') if kwargs.get('atk_two_name') else "Secondary"
        self.atk_three_name = kwargs.get('atk_three_name') if kwargs.get('atk_three_name') else "Ultimate Attack"

    def attack_one(self):
        total = self.current_attack
        result = f"The {self.name} uses their basic attack."
        if self.attack_roll() > 85:
            result += " It is a critical hit!!!"
        result += f"\nThe attack causes {total} damage."
        return self.result_string(result, total)

    def attack_two(self):
        result = f"The {self.name} gains focus and increases their attack!"
        self.current_attack = ceil(self.current_attack * 1.5)
        return self.result_string(result, 0)

    def attack_three(self):
        total = self.current_attack * 2
        result = f"The {self.name} uses their ultimate attack for {total} damage!"
        return self.result_string(result, 0)

    def gets_hit(self, damage, ignore_defense=False):
        total = damage - self.current_defense if not ignore_defense else damage
        result = "\n"
        if total < 0:
            total = 0
        elif total > 0 and self.attack_roll() > 95:
            result += "The attack missed! "
            total = 0
        result += f"The {self.name} takes {total} damage."
        self.current_health -= total
        return result

    # Utility methods
    def heal_self(self, amount):
        self.current_health += amount
        if self.current_health > self.health:
            self.current_health = self.health

    @staticmethod
    def attack_roll():
        return randint(1, 100)

    @staticmethod
    def result_string(results, total, ignore=False):
        result = "\n" + results
        return result, total, ignore

    @staticmethod
    def set_stat(level, stat, default_stat):
        if stat:
            return ceil(stat * level)
        else:
            return ceil(default_stat * level)


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
        self.current_spirit = 0
        self.spirit_regen = kwargs.get('spirit_regen') or 2
        self.experience = 0
        self.atk_two_req = kwargs.get('atk_two_req') or 2
        self.atk_three_req = kwargs.get('atk_three_req') or 3
        self.def_chance = kwargs.get('def_chance') or 80
        self.current_def_chance = self.def_chance

    def refresh_spirit(self):
        self.current_spirit += self.spirit_regen
        if self.current_spirit > self.spirit:
            self.current_spirit = self.spirit
        return f"\nThe {self.name} regenerates {self.spirit_regen} spirit points."

    def call_attack(self, choice):
        if choice == '1':
            return self.attack_one()
        elif choice == '2':
            self.current_spirit -= self.atk_two_req
            return self.attack_two()
        elif choice == '3':
            self.current_spirit -= self.atk_three_req
            return self.attack_three()

    def defend(self):
        self.current_def_chance -= 10
        result = "\n"
        if self.attack_roll() <= self.current_def_chance:
            result += f"\nThe {self.name} takes a defensive stance and successfully avoids all damage."
            return True, result
        else:
            result += f"\nThe {self.name} takes a defensive stance but fails to defend from the attack."
            return False, result

    def attack_one(self):
        result = super().attack_one()
        log_result = result[0] + self.refresh_spirit()
        return log_result, result[1], result[2]

    def battle_reset(self):
        self.current_attack = self.attack
        self.current_defense = self.defense
        self.current_def_chance = self.def_chance

    def get_experience(self, monster_level):
        level_difference = self.level - monster_level
        total_exp = 20 - (level_difference * 2)
        if total_exp < 1:
            total_exp = 1
        elif total_exp > 40:
            total_exp = 40
        self.experience += total_exp
        return self.level_up()

    def level_up(self):
        if self.experience > 99:
            self.health = int(self.health / self.level * (self.level + 1))
            self.attack = int(self.attack / self.level * (self.level + 1))
            self.defense = int(self.defense / self.level * (self.level + 1))
            self.current_health = self.health
            self.current_attack = self.current_attack if self.current_attack > self.attack else self.attack
            self.current_defense = self.current_defense if self.current_defense > self.defense else self.defense
            self.level += 1
            self.experience -= 100
            return "\nYou leveled up! Your feel refreshed!"
        return ""
