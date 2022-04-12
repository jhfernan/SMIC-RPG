from data.characters import Player


# Heroes have a general stat breakdown of the following:
# 12 total stat points for pure stat heavy heroes
# 10 for average total stats plus some utility
# 8 for the lower stats with heavy utility
# Spirit is not included in the stats total but can factor into the utility that it adds


class Paladin(Player):

    def __init__(self, level=1):
        super().__init__(level=level,
                         attack=4,
                         defense=1,
                         def_chance=110,
                         spirit=3,
                         spirit_regen=1,
                         name="Paladin")

    def attack_two(self):
        total = self.current_attack
        if self.attack_roll() > 70:
            total *= 2
        self.heal_self(total)
        return self.result_string(f"The {self.name} heals for {total} health", 0)

    def attack_three(self):
        total = self.attack * 2
        return self.result_string(f"The {self.name} does a double-strike for {total} damage", total)


class Assassin(Player):

    def __init__(self, level=1):
        super().__init__(level=level,
                         health=5,
                         attack=6,
                         def_chance=60,
                         spirit=4,
                         spirit_regen=2,
                         atk_two_req=1,
                         atk_three_req=4,
                         name="Assassin")
        self.focus = 60

    def gets_hit(self, damage, ignore_defense=False):
        if self.attack_roll() > 50:
            return f"\nThe swift {self.name} blends into the shadows and the attacks misses!"
        else:
            return super().gets_hit(damage, ignore_defense)

    def attack_two(self):
        result = f"The {self.name} retreats into the shadows to gain focus and blend into the darkness"
        self.focus += 15
        self.current_defense += self.level
        return self.result_string(result, 0)

    def attack_three(self):
        result = f"The {self.name} strikes from the shadows!"
        total = self.current_attack * 2
        if self.attack_roll() < self.focus:
            result += " The sneak attack is successful!"
            total *= 2
        result += f"\nThe {self.name} strikes its target from behind for {total} damage"
        self.focus = 60
        return self.result_string(result, total)
