import math
import sys
import tkinter as tk
from tkinter import messagebox

import Constants
from Player import Player


class BoardGui:
    def __init__(self, game_controller):
        self.game_controller = game_controller

        self.PADDING = 5
        self.FIELD_SIZE = 40

        self.to_be_deleted = []
        self.field_id_last_move = None

        self.occupied_fields = []
        self._make_occupied_field()
        self._draw_board()

        self.human_may_play = False

    def _make_occupied_field(self):
        self.occupied_fields = []
                
        for r in range(0, Constants.BOARD_SIZE):
            self.occupied_fields.append([])
            for c in range(0, Constants.BOARD_SIZE):
                self.occupied_fields[r].append(False)

    def _draw_board(self):
        self.root = tk.Tk()
        board = tk.Frame(self.root)
        board.pack()

        board.bind('<Button-1>', self.exit_game)

        self.board_canvas = tk.Canvas(board,
                                      width=Constants.BOARD_SIZE * self.FIELD_SIZE + 10,
                                      height=Constants.BOARD_SIZE * self.FIELD_SIZE + 10,
                                      bg=Constants.BACKGROUND_COLOR)

        self.board_canvas.pack()
        self.board_canvas.bind("<Button-1>", self.canvas_callback)

        for r in range(0, Constants.BOARD_SIZE + 1):
            self.board_canvas.create_line(r * self.FIELD_SIZE + self.PADDING,
                                          self.PADDING,
                                          r * self.FIELD_SIZE + self.PADDING,
                                          Constants.BOARD_SIZE * self.FIELD_SIZE + self.PADDING)
            self.board_canvas.create_line(self.PADDING,
                                          r * self.FIELD_SIZE + self.PADDING,
                                          Constants.BOARD_SIZE * self.FIELD_SIZE + self.PADDING,
                                          r * self.FIELD_SIZE + self.PADDING)

    def start_loop(self):
        self.root.mainloop()

    def _fill_start_position(self):
        player1 = Player(Constants.PLAYER1)
        player2 = Player(Constants.PLAYER2)

        index = Constants.BOARD_SIZE // 2
        self.place_stone(index - 1, index - 1, player1)
        self.place_stone(index - 1, index, player2)
        self.place_stone(index, index - 1, player2)
        self.place_stone(index, index, player1)

    def mark_computer_move(self, row, column):
        self.unmark_move()

        x0 = column * self.FIELD_SIZE + self.PADDING
        y0 = row * self.FIELD_SIZE + self.PADDING
        x1 = x0 + self.FIELD_SIZE
        y1 = y0 + self.FIELD_SIZE
        self.field_id_last_move = self.board_canvas.create_rectangle(x0, y0, x1, y1, fill=Constants.MOVE_COLOR)

    def unmark_move(self):
        if self.field_id_last_move is not None:
            self.board_canvas.delete(self.field_id_last_move)
            self.field_id_last_move = None

    def place_stone(self, row, column, player):
        if row >= Constants.BOARD_SIZE or row < 0 or column >= Constants.BOARD_SIZE or column < 0:
            # User clicked just outside the bord.
            return

        self.undo_set_selectable_fields()
        centery = math.ceil(self.PADDING + row * self.FIELD_SIZE + 2)
        centerx = math.ceil(self.PADDING + column * self.FIELD_SIZE + 2)

        self.board_canvas.create_oval(centerx, centery,
                                      centerx + self.FIELD_SIZE - 4,
                                      centery + self.FIELD_SIZE - 4,
                                      fill=player.color)

        self.occupied_fields[row][column] = True

    def set_selectable_field(self, row, column):
        x0 = column * self.FIELD_SIZE + self.PADDING
        y0 = row * self.FIELD_SIZE + self.PADDING
        x1 = x0 + self.FIELD_SIZE
        y1 = y0 + self.FIELD_SIZE

        rect_id = self.board_canvas.create_rectangle(x0, y0, x1, y1, fill=Constants.SELECTABLE_COLOR)
        self.to_be_deleted.append(rect_id)

    def undo_set_selectable_fields(self):
        for widget_id in self.to_be_deleted:
            self.board_canvas.delete(widget_id)

    def canvas_callback(self, event):
        if not self.human_may_play:
            return

        c = (event.x - self.PADDING) // self.FIELD_SIZE
        r = (event.y - self.PADDING) // self.FIELD_SIZE
        self.game_controller.place_request_human_stone(r, c)

    def exit_game(self, event):
        sys.exit(1)

    def set_human_may_play(self, value):
        self.human_may_play = value

    def does_human_starts(self):
        answer = self.yes_no_question("Wil jij beginnen?")
        return answer == 'yes'

    def yes_no_question(self, question):
        return tk.messagebox.askquestion(message=question)
        # 'yes' of 'no'

    def game_end(self):
        self.ok_message("Game is finished.")

    def ok_message(self, message):
        return tk.messagebox.showinfo(message=message)
