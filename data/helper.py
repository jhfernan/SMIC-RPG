import os


class Helper:
    screen_width = 72

    @staticmethod
    def clear_screen():
        """To clear the screen when playing in terminal"""
        if os.name == "nt":
            os.system('cls')
        else:
            os.system('clear')

    def setup_screen(self, title=None):
        self.set_title_component(title=title) if title else self.set_title_component()

    def set_title_component(self, title="MY RPG"):
        self.clear_screen()
        screen = "*" * self.screen_width
        screen += f"\n\n{self.center_text(title)}\n\n" + ('*' * self.screen_width)
        screen += "\n"
        print(screen)

    def center_text(self, string):
        length_of_string = len(string)
        if length_of_string >= self.screen_width - 1:
            return string
        else:
            leftover = round((self.screen_width - length_of_string) / 2)
            return f"{leftover * ' '}{string}"

    def set_column_string(self, string):
        width = round(self.screen_width / 2)
        leftover = width - len(string)
        return string + (leftover * " ")

    def hr(self):
        return "*" * self.screen_width
