from random import choice
from data.characters import Monster

# Monsters have a general stat breakdown of the following:
# 12 total stat points for best monsters
# 10 for average total stats
# 8 for the lower units


# Easy Monsters - For Gaming Journalists
class Zombie(Monster):

    def __init__(self, level):
        super().__init__(level=level, health=3, attack=5, name='Zombie')

    def attack_two(self):
        total = round(self.current_attack * 0.75)
        result = f"The {self.name} takes a bite out of you. He deals and heals for {total} damage"
        self.heal_self(total)
        return self.result_string(result, total)


class Slime(Monster):

    def __init__(self, level):
        super().__init__(level=level, health=4, attack=3, defense=1, name='Slime')

    def attack_two(self):
        total = self.current_attack
        self.heal_self(total)
        self.current_defense += self.level
        return self.result_string(f"The {self.name} heals for {total} and raises his defenses", 0)

    def attack_three(self):
        total = round(self.current_attack * 1.5)
        return self.result_string(f"The {self.name} bypasses your defense for {total} damage", total, True)


# Medium Difficulty Monsters
class SpineLauncher(Monster):

    def __init__(self, level):
        super().__init__(level=level, health=5.5, attack=4, defense=1.25, name='Spine Launcher')

    def attack_one(self, amount_of_attacks=2):
        result = f"Spine Launcher fires {amount_of_attacks} spikes towards you!"
        total = 0
        for _ in range(amount_of_attacks):
            does_it_hit = choice([True, False])
            if does_it_hit:
                result += f" A Spike hits its mark for {self.current_attack} damage!"
                total += self.current_attack
            else:
                result += " The spike misses."
        return self.result_string(result, total)

    def attack_two(self, amount_of_attacks=3):
        return self.attack_one(amount_of_attacks=4)

    def attack_three(self):
        return self.attack_two(amount_of_attacks=6)


# Hard/Boss Difficulty Monsters
