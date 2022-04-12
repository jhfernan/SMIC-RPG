from data.battle_engine import BattleEngine


class Game(BattleEngine):

    def __init__(self, level=1):
        super().__init__(level)
        self.start_game()

    def start_game(self):
        while self.keep_playing:
            self.battle()
        print("Thanks for playing!")
