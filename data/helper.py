import os


class Helper:

    @staticmethod
    def clear_screen():
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    @staticmethod
    def set_title_component():
        screen = '*' * 72
        screen += '\n\t\t\tMY RPG\n\n' + ('*' * 72)
        screen += '\n'
        print(screen)
