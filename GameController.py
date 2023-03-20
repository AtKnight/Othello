import threading
import sys
import Constants

from BoardGui import BoardGui
from BoardData import BoardData
from Player import Player
from time import sleep


class GameController:
    def __init__(self):
        self.board_gui = BoardGui(self)

        self.board_data = BoardData(self.board_gui)
        self.board_data.place_stones_start_position()

        self.human_player = None
        self.computer_player = None

        self.playable_fields = []
        self.last_computer_move = None  # (row, column)

    def start_game(self):
        if self.board_gui.does_human_starts():
            self.human_player = Player(Constants.PLAYER1)
            self.computer_player = Player(Constants.PLAYER2)

            self.human_play()
        else:
            self.computer_player = Player(Constants.PLAYER1)
            self.human_player = Player(Constants.PLAYER2)

            self.computer_play_random_move()
            self.human_play()

        self.board_gui.start_loop()

    def human_play(self):
        self.board_gui.set_human_may_play(Constants.SHOW)
        self.playable_fields = self.board_data.get_playable_fields(self.human_player)

        if len(self.playable_fields) > 0:
            self.show_playable_fields(self.playable_fields)
        elif self.board_data.game_finished(self.computer_player):
            self.board_gui.message_game_end()
        else:
            self.board_gui.ok_message("Human cannot move, computer is thinking.")
            self.start_thread_computer_move()

    def computer_play_random_move(self):
        row, column = self.board_data.get_random_move(self.computer_player)

        if row is None or column is None:
            self.board_gui.ok_message("Computer cannot make a valid random move.")

            sys.exit(1)

        self.computer_play_move(row, column)

    def computer_play_move(self, row, column):
        self.board_gui.mark_computer_move(row, column)
        self.board_data.execute_move(row, column, self.computer_player, Constants.SHOW)

    def show_playable_fields(self, playable_fields):
        if len(playable_fields) == 0:
            self.board_gui.ok_message("There are no valid move to show.")

            sys.exit(1)

        for row, column in playable_fields:
            self.board_gui.set_selectable_field(row, column)

    def place_request_human_stone(self, row, column):
        if (row, column) in self.playable_fields:
            file = open(Constants.FILENAME_PLAYED_MOVES, 'a')
            file.write(f"{row} {column}\n")
            file.close()

            self.board_gui.mark_computer_move(row, column)
            self.board_data.execute_move(row, column, self.human_player, Constants.SHOW)

            self.playable_fields = []

            if self.board_data.game_finished(self.human_player):
                self.board_gui.game_end()
            else:
                if len(self.board_data.get_playable_fields(self.computer_player)) > 0:
                    self.start_thread_computer_move()
                else:
                    self.board_gui.ok_message("Computer cannot place a stone")
                    self.human_play()

    def start_thread_computer_move(self):
        threading.Thread(target=self.play_next_computer_move, name="computer_move").start()

    def play_next_computer_move(self):
        white_stones, black_stones = self.board_data.number_of_stones()
        number_of_stones = white_stones + black_stones

        if number_of_stones < Constants.END_STONES:
            depth = Constants.NORMAL_DEPTH
            final_state = False
        else:
            depth = Constants.BOARD_SIZE * Constants.BOARD_SIZE - number_of_stones
            final_state = True

        speler, beste_zet, waarde = self.board_data.alpha_beta(depth, depth, +-10000, 10000, self.computer_player, final_state)
        print("result alpha-beta ", speler, beste_zet, waarde)
        if not (speler == self.computer_player):
            self.board_gui.ok_message("computer cannot play. NOG OPLOSSEN")

        self.board_gui.mark_computer_move(beste_zet[0], beste_zet[1])
        self.board_data.execute_move(beste_zet[0], beste_zet[1], self.computer_player, Constants.SHOW)

        white_stones, black_stones = self.board_data.number_of_stones()
        print(f"aantal witte en zwarte stenen: {white_stones}  {black_stones}")

        if self.board_data.game_finished(self.human_player):
            self.board_gui.game_end()
        else:
            self.human_play()

    def ok_message(self, message):
        self.board_gui.ok_message(message)
