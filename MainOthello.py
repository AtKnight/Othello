import Constants

from GameController import GameController

if __name__ == '__main__':
    file = open(Constants.FILENAME_PLAYED_MOVES, 'w')
    # Makes file empty
    file.close()

    game_controller = GameController()
    game_controller.start_game()


