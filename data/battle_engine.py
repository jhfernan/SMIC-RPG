from random import randint
from math import ceil
from data.helper import Helper
from data.characters import Player
from data.heroes import Paladin, Assassin
from data.monsters import Slime, SpineLauncher, Zombie


class BattleEngine(Helper):

    def __init__(self, level):
        super().__init__()
        self.keep_playing = True
        self.setup_screen()
        self.player = self.choose_class(level)
        self.monster = Slime(level=self.player.level)
        self.monster_kill_count = 0
        self.log = ""

    def battle(self):
        self.player.battle_reset()
        while self.check_if_both_alive():
            self.battle_screen()
            player_choice = input("Choose a move.\n>>> ")
            if not self.validate_option(choice=player_choice):
                print(self.center_text("Not a valid choice."))
                input("Press any key to continue\n>>> ")
                continue
            self.process_battle(player_choice)
        if self.player.current_health < 1:
            self.game_over_screen()
        elif self.monster.current_health < 1:
            self.monster_kill_count += 1
            self.victory_screen()

    def battle_screen(self):
        self.set_title_component(title=f"{self.player.name} vs {self.monster.name}")
        self.characters_screen()
        if len(self.log) > 0:
            print(f"{self.log}\n\n{self.hr()}")

    def characters_screen(self):
        player_attack_string = self.return_stat_string(self.player.attack, self.player.current_attack)
        monster_attack_string = self.return_stat_string(self.monster.attack, self.monster.current_attack)
        player_defense_string = self.return_stat_string(self.player.defense, self.player.current_defense)
        monster_defense_string = self.return_stat_string(self.monster.defense, self.monster.current_defense)
        result_string = self.set_column_string(f"LV{self.player.level} {self.player.name}")
        result_string += self.set_column_string(f"LV{self.monster.level} {self.monster.name}") + "\n"
        result_string += self.set_column_string(f"HP: {self.player.current_health}/{self.player.health}")
        result_string += self.set_column_string(f"HP: {self.monster.current_health}/{self.monster.health}") + "\n"
        result_string += self.set_column_string(f"SP: {self.player.current_spirit}/{self.player.spirit}")
        result_string += self.set_column_string(f"ATK: {monster_attack_string}") + "\n"
        result_string += self.set_column_string(f"ATK: {player_attack_string}")
        result_string += self.set_column_string(f"DEF: {monster_defense_string}") + "\n"
        result_string += self.set_column_string(f"DEF: {player_defense_string}") + '\n'
        result_string += self.set_column_string(f"EXP: {self.player.experience}/100") + '\n'
        result_string += "**********\n"
        result_string += f"1 | {self.player.atk_one_name} (0 SP)\n"
        result_string += f"2 | {self.player.atk_two_name} ({self.player.atk_two_req} SP)\n"
        result_string += f"3 | {self.player.atk_three_name} ({self.player.atk_three_req} SP)\n"
        result_string += "4 | Defend\n"
        result_string += self.hr()
        print(result_string)

    def game_over_screen(self, died=True):
        self.set_title_component(title="Game Over")
        final = "You have died!" if died else f"You defeated {self.monster_kill_count} monster(s)!"
        final += "\nFinal Stats:"
        final += f"\n{self.player.name} lvl {self.player.level}"
        final += f"\nHP:{self.player.health}"
        final += f"\nATK:{self.player.attack}"
        final += f"\nDEF:{self.player.defense}"
        final += f"\nCurrent Monster Kill Count: {self.monster_kill_count}"
        print(final)
        self.keep_playing = False

    def victory_screen(self):
        self.set_title_component(title=f"You defeated the {self.monster.name}")
        healing_amount = ceil(self.player.health / 3)
        self.player.heal_self(healing_amount)
        question_prompt = f"Current Monster Kill Count: {self.monster_kill_count}"
        question_prompt += f"\nYou rest after the battle and recover {healing_amount} health"
        question_prompt += "\nDo you wish to continue? (Y, n)\n>>> "
        response = input(question_prompt)
        if response.lower() == "n":
            self.keep_playing = False
            self.game_over_screen(died=False)
        else:
            self.pick_monster()

    def process_battle(self, choice):
        if choice == '4':
            response = self.player.defend()
            self.log += response[1]
            if response[0]:
                self.log += self.monster.attack_choice()[0]
                self.log += f"\nThe {self.monster.name} fails to inflict damage because of the defensive stance."
            else:
                mon_result = self.monster.attack_choice()
                self.log += mon_result[0]
                self.log += self.player.gets_hit(damage=mon_result[1], ignore_defense=mon_result[2])
        else:
            play_result = self.player.call_attack(choice)
            self.log += play_result[0]
            self.log += self.monster.gets_hit(damage=play_result[1], ignore_defense=play_result[2])
            if self.monster.current_health > 0:
                mon_result = self.monster.attack_choice()
                self.log += mon_result[0]
                self.log += self.player.gets_hit(damage=mon_result[1], ignore_defense=mon_result[2])
            else:
                self.log += f"\nThe {self.monster.name} falls to the ground, dead!"
        if self.player.current_health > 0:
            self.log += self.player.get_experience(self.monster.level)
        self.battle_screen()
        input("Next >>> ")
        self.log = ""

    def choose_class(self, level):
        player_char_prompt = "What character do you want to play? (Please input a number)\n"
        player_char_prompt += "1 - Paladin (Easy Difficulty)\n"
        player_char_prompt += "2 - Assassin (Hard Difficulty)\n"
        player_char_prompt += "Q - Quit\n"
        player_char_prompt += ">>> "
        choice = input(player_char_prompt)
        if choice == '1':
            return Paladin(level=level)
        elif choice == '2':
            return Assassin(level=level)
        else:
            self.keep_playing = False
            return Player(level=level)

    def pick_monster(self):
        pick = randint(1, 10)
        if pick == 1:
            self.monster = Slime(level=self.pick_monster_level())
        elif pick == 2:
            self.monster = SpineLauncher(level=self.pick_monster_level())
        elif pick == 3:
            self.monster = Zombie(level=self.pick_monster_level())
        else:
            self.monster = Slime(level=self.pick_monster_level())

    def check_if_both_alive(self):
        if self.player.current_health > 0 and self.monster.current_health > 0:
            return True
        else:
            return False

    def validate_option(self, choice):
        if choice == '1' or choice == '4':
            return True
        elif choice == '2' and self.player.current_spirit >= self.player.atk_two_req:
            return True
        elif choice == '3' and self.player.current_spirit >= self.player.atk_three_req:
            return True
        else:
            return False

    def pick_monster_level(self):
        allowed_difference = ceil(self.player.level / 5)
        level = randint(self.player.level - allowed_difference, self.player.level + allowed_difference)
        if level < 1:
            level = 1
        return level

    @staticmethod
    def return_stat_string(stat=3, c_stat=3):
        if stat < c_stat:
            return f"+{c_stat}"
        elif stat == c_stat:
            return c_stat
        else:
            return f"-{c_stat}"
