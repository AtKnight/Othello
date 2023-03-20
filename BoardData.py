import copy
import random
import Constants
import sys

from FieldContent import FieldContent
from Player import Player
from Stack import Stack


class BoardData:
    def __init__(self, game_controller,  board_matrix=None):
        self.game_controller = game_controller
        self.board_matrix = None
        # Makes Pycharm happy

        if board_matrix is None:
            self.board_matrix = self._create_board_matrix()
            self._set_field_values()
            for r in range(0, Constants.BOARD_SIZE):
                for c in range(0, Constants.BOARD_SIZE):
                    print(f"({r}, {c}) {self.board_matrix[r][c].value:3}  ", end="")
                print()
        else:
            self.board_matrix = copy.deepcopy(board_matrix)


    def _create_board_matrix(self):
        board_matrix = []

        for r in range(0, Constants.BOARD_SIZE):
            row = []
            for c in range(0, Constants.BOARD_SIZE):
                row.append(FieldContent())
                # empty field

            board_matrix.append(row)
        return board_matrix

    def _set_field_values(self):
        for r in range(0, Constants.BOARD_SIZE):
            for c in range(0, Constants.BOARD_SIZE):
                self.board_matrix[r][c].set_value(0)

        m = self.board_matrix
        # a shorthand

        # row 0
        m[0][0].value = m[0][Constants.BOARD_SIZE - 1].value = Constants.A
        m[Constants.BOARD_SIZE - 1][0].value = m[Constants.BOARD_SIZE - 1][Constants.BOARD_SIZE - 1].value = \
            Constants.A

        m[0][1].value = m[0][Constants.BOARD_SIZE - 2].value = Constants.B
        m[Constants.BOARD_SIZE - 1][1].value = m[Constants.BOARD_SIZE - 1][Constants.BOARD_SIZE - 2].value = \
            Constants.B

        m[0][2].value = m[0][Constants.BOARD_SIZE - 3].value = Constants.C
        m[Constants.BOARD_SIZE - 1][2].value = m[Constants.BOARD_SIZE - 1][Constants.BOARD_SIZE - 3].value = \
            Constants.C

        # row 1
        m[1][0].value = m[1][Constants.BOARD_SIZE - 1].value = Constants.B
        m[Constants.BOARD_SIZE - 2][0].value = m[Constants.BOARD_SIZE - 2][Constants.BOARD_SIZE - 1].value = \
            Constants.B

        m[1][1].value = m[1][Constants.BOARD_SIZE - 2].value = Constants.D
        m[Constants.BOARD_SIZE - 2][1].value = m[Constants.BOARD_SIZE - 2][Constants.BOARD_SIZE - 2].value = \
            Constants.D

        m[1][2].value = m[1][Constants.BOARD_SIZE - 3].value = Constants.E
        m[Constants.BOARD_SIZE - 2][2].value = m[Constants.BOARD_SIZE - 2][Constants.BOARD_SIZE - 3].value = \
            Constants.E

        # row 2
        m[2][0].value = m[2][Constants.BOARD_SIZE - 1].value = Constants.C
        m[Constants.BOARD_SIZE - 3][0].value = m[Constants.BOARD_SIZE - 3][Constants.BOARD_SIZE - 1].value = \
            Constants.C

        m[2][1].value = m[2][Constants.BOARD_SIZE - 2].value = Constants.F
        m[Constants.BOARD_SIZE - 3][1].value = m[Constants.BOARD_SIZE - 3][Constants.BOARD_SIZE - 2].value = \
            Constants.E

        m[2][2].value = m[2][Constants.BOARD_SIZE - 3].value = Constants.F
        m[Constants.BOARD_SIZE - 3][2].value = m[Constants.BOARD_SIZE - 3][Constants.BOARD_SIZE - 3].value = \
            Constants.E

    def alpha_beta(self, depth, start_depth, alpha, beta, player, final_state):
        if depth == 0 or self.game_finished(player):
            return player, None, self.node_value(player, final_state)

        best_field = None
        opponent = player.get_opponent()
        playable_fields = self.get_playable_fields(player)

        if len(playable_fields) == 0:
            # Not end of game!, but player can not play.
            # Other player may make a move again.
            return self.alpha_beta(depth, start_depth, -beta, -alpha, opponent, final_state)
            # returns player_color, best_reaction, value

        # sorteer playable_field
        # ======================

        copy_board_matrix = copy.deepcopy(self.board_matrix)

        for field in playable_fields:  # (r, c)
            self.execute_move(field[0], field[1], player, Constants.SHOWNOT)

            player_color, best_reaction, value = \
                self.alpha_beta(depth - 1, start_depth, -beta, -alpha, opponent, final_state)

            self.board_matrix = copy.deepcopy(copy_board_matrix)

            if start_depth - depth < 7:
                print(f"depth = {depth}, value = {value}, field = {field}, alpha = {alpha}, best_field = {best_field}")

            if value > alpha:
                alpha = value
                best_field = field

            if alpha >= beta:
                break

        return player, best_field, alpha
    
    def game_finished(self, player):
        if self.player_can_move(player):
            return False

        opponent = player.get_opponent()
        return not self.player_can_move(opponent)

    def player_can_move(self, player):
        return len(self.get_playable_fields(player)) > 0

    # -------------------------------------------------------------------------------------

    def is_playable_field(self, row, column, player):
        # May player place his stone in (row, colum)?

        if not self.board_matrix[row][column].is_empty():
            return False

        # direction: left_up
        #       up
        #       right_up
        #       right
        #       right_below
        #       below
        #       left_below
        #       left
        for delta_c in range(-1, 2):
            for delta_r in range(-1, 2):
                if self.search_player_in_direction(delta_r, delta_c, row, column, player):
                    return True
        return False

    def search_player_in_direction(self, delta_r, delta_c, row, column, player):
        row += delta_r
        column += delta_c

        # first field should be occupied by other_player
        if not self.is_valid_coord(row, column):
            return False

        field = self.board_matrix[row][column]
        if field.is_empty():
            return False

        if field.is_occupied_by(player):
            return False

        # field is occupied by other_player
        # try next fields

        while True:
            row += delta_r
            column += delta_c

            if not self.is_valid_coord(row, column):
                return False

            field = self.board_matrix[row][column]

            if field.is_empty():
                return False

            if field.is_occupied_by(player):
                return True

            # field is occupied by other_player
            # try next field

    # -------------------------------------------------------------------------------------

    def place_stones_start_position(self):
        index = Constants.BOARD_SIZE // 2

        self.place_stone(index - 1, index - 1, Player(Constants.PLAYER2), Constants.SHOW)
        self.place_stone(index - 1, index, Player(Constants.PLAYER1), Constants.SHOW)
        self.place_stone(index, index - 1, Player(Constants.PLAYER1), Constants.SHOW)
        self.place_stone(index, index, Player(Constants.PLAYER2), Constants.SHOW)

    def place_stone(self, row, column, player, place_on_gui):
        # self.board_matrix[row][column] = FieldContent(player)
        self.board_matrix[row][column].place_stone(player)

        if place_on_gui:
            self.game_controller.place_stone(row, column, player)

    # -------------------------------------------------------------------------------------

    def execute_move(self, row, column, player, place_on_gui):
        # Place and flip all stones of player caused by placing a stone at (row, column).
        # Pre-condition: move is legal
        # ============================

        if not self.board_matrix[row][column].is_empty():
            # should not happen
            print("execute_move: This cannot happen ....", self.board_matrix[row][column])
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
            return False

        self.place_stone(row, column, player, place_on_gui)

        # direction: left_up
        #       right_up
        #       right
        #       right_below
        #       below
        #       left_below
        #       left

        stones_placed = False
        for delta_c in range(-1, 2):
            for delta_r in range(-1, 2):
                if self.execute_moves_in_direction(delta_r, delta_c, row, column, player, place_on_gui):
                    stones_placed = True

        # should not be False
        if not stones_placed:
            print("execute_move: This can not happen, no stones are placed. row, column: ", row, column)

            self.game_controller.ok_message("FOUT EINDE")
            sys.exit(1)

        return stones_placed

    def execute_moves_in_direction(self, delta_r, delta_c, start_row, start_column, player, place_on_gui):
        row = start_row + delta_r
        column = start_column + delta_c

        # first field should be occupied by other_player
        if not self.is_valid_coord(row, column):
            return False

        field = self.board_matrix[row][column]
        if field.is_empty():
            return False

        if field.is_occupied_by(player):
            return False

        # field is occupied by other_player
        # try next fields

        while True:
            row += delta_r
            column += delta_c

            if not self.is_valid_coord(row, column):
                return False

            field = self.board_matrix[row][column]

            if field.is_empty():
                return False

            if field.is_occupied_by(player):
                r = start_row + delta_r
                c = start_column + delta_c

                while not (r == row and c == column):
                    self.place_stone(r, c, player, place_on_gui)
                    r += delta_r
                    c += delta_c

                return True
            # else doorgaan met zoeken in deze richting.

        # print("This statement can not be executed.")
        # return False

    # -------------------------------------------------------------------------------------

    def is_valid_coord(self, row, column):
        return 0 <= row < Constants.BOARD_SIZE and \
               0 <= column < Constants.BOARD_SIZE

    # -------------------------------------------------------------------------------------

    def node_value(self, player, final_state):
        # advantage for PLAYER1(Black) is negative.
        # ========================================
        # advantage for PLAYER2(White) is positive.
        # ========================================

        number_white_stones, number_black_stones = self.number_of_stones()
        result = 0

        if final_state:
            return number_white_stones - number_black_stones

        result = number_black_stones - number_white_stones

        #result += self.value_fields()

        return result

    def get_playable_fields(self, player): # --> [(r,c)]
        result = []

        for r in range(0, Constants.BOARD_SIZE):
            for c in range(0, Constants.BOARD_SIZE):
                if self.is_playable_field(r, c, player):
                    result.append((r, c))
        return result

    def get_random_move(self, player): # --> (r, c)
        possible_fields = self.get_playable_fields(player)
        length = len(possible_fields)

        if length == 0:
            # There are no valid moves for player
            return None, None #(row, column)

        index = random.randint(0, length - 1)

        return possible_fields[index]  # (row, column)

    def number_of_stones(self):  # --> (c1, c2)
        count1 = 0
        count2 = 0

        for r in range(0, Constants.BOARD_SIZE):
            for c in range(0, Constants.BOARD_SIZE):
                field = self.board_matrix[r][c]
                if not field.is_empty():
                    if field.contains_player2():
                        count1 += 1
                    else:
                        count2 += 1

        return count1, count2

    def value_fields(self):
        result = self.value_corner(self.board_matrix[0][0], self.board_matrix[0][1], self.board_matrix[0][2],
                                   self.board_matrix[1][0], self.board_matrix[1][1], self.board_matrix[1][2],
                                   self.board_matrix[2][0], self.board_matrix[2][1], self.board_matrix[2][2])

        result += self.value_corner(self.board_matrix[0][Constants.BOARD_SIZE - 1],
                                    self.board_matrix[0][Constants.BOARD_SIZE - 2],
                                    self.board_matrix[0][Constants.BOARD_SIZE - 3],
                                    self.board_matrix[1][Constants.BOARD_SIZE - 1],
                                    self.board_matrix[1][Constants.BOARD_SIZE - 2],
                                    self.board_matrix[1][Constants.BOARD_SIZE - 3],
                                    self.board_matrix[2][Constants.BOARD_SIZE - 1],
                                    self.board_matrix[2][Constants.BOARD_SIZE - 2],
                                    self.board_matrix[2][Constants.BOARD_SIZE - 3])

        result += self.value_corner(self.board_matrix[Constants.BOARD_SIZE - 1][0],
                                    self.board_matrix[Constants.BOARD_SIZE - 1][1],
                                    self.board_matrix[Constants.BOARD_SIZE - 1][2],
                                    self.board_matrix[Constants.BOARD_SIZE - 2][0],
                                    self.board_matrix[Constants.BOARD_SIZE - 2][1],
                                    self.board_matrix[Constants.BOARD_SIZE - 2][2],
                                    self.board_matrix[Constants.BOARD_SIZE - 3][0],
                                    self.board_matrix[Constants.BOARD_SIZE - 3][1],
                                    self.board_matrix[Constants.BOARD_SIZE - 3][2])

        result += self.value_corner(self.board_matrix[Constants.BOARD_SIZE - 1][Constants.BOARD_SIZE - 1],
                                    self.board_matrix[Constants.BOARD_SIZE - 1][Constants.BOARD_SIZE - 2],
                                    self.board_matrix[Constants.BOARD_SIZE - 1][Constants.BOARD_SIZE - 3],
                                    self.board_matrix[Constants.BOARD_SIZE - 2][Constants.BOARD_SIZE - 1],
                                    self.board_matrix[Constants.BOARD_SIZE - 2][Constants.BOARD_SIZE - 2],
                                    self.board_matrix[Constants.BOARD_SIZE - 2][Constants.BOARD_SIZE - 3],
                                    self.board_matrix[Constants.BOARD_SIZE - 3][Constants.BOARD_SIZE - 1],
                                    self.board_matrix[Constants.BOARD_SIZE - 3][Constants.BOARD_SIZE - 2],
                                    self.board_matrix[Constants.BOARD_SIZE - 3][Constants.BOARD_SIZE - 3])
        """ 

        if not self.board_matrix[0][0].is_empty() or not self.board_matrix[Constants.BOARD_SIZE - 1][0].is_empty():
            result += self.count_stones_edge_vertical(0)

        if not self.board_matrix[0][Constants.BOARD_SIZE - 1].is_empty() or \
                not self.board_matrix[Constants.BOARD_SIZE - 1][Constants.BOARD_SIZE - 1].is_empty():
            result += self.count_stones_edge_vertical(Constants.BOARD_SIZE - 1)

        if not self.board_matrix[0][0].is_empty() or not self.board_matrix[0][Constants.BOARD_SIZE - 1].is_empty():
            result += self.count_stones_edge_horizontal(0)

        if not self.board_matrix[Constants.BOARD_SIZE - 1][0].is_empty() or \
                not self.board_matrix[Constants.BOARD_SIZE - 1][Constants.BOARD_SIZE - 1].is_empty():
            result += self.count_stones_edge_horizontal(Constants.BOARD_SIZE - 1)
        """
        return result

    def value_corner(self, f00, f01, f02,
                           f10, f11, f12,
                           f20, f21, f22):
        # f00 corresponds to the corner

        if not f00.is_empty():
            print("tel elders velden langs de rand")
            if f00.is_occupied_by(Player(Constants.PLAYER1)):
                return -10
            else:
                return 10

        # corner is empty

        if f11.is_empty():
            pass
        else:
            if f11.is_occupied_by(Player(Constants.PLAYER1)):
                return 10
            else:
                return  -8

        return 0


        #     result = f22.get_value()
        #
        #     if f10.is_empty():
        #         result += f20.get_value() + f12.get_value()
        #     else:
        #         result += f10.get_value()
        #
        #     if f01.is_empty():
        #         result += f02.get_value() + f21.get_value()
        #     else:
        #         result += f01.get_value()
        #
        # else:
        #     # f00 is empty and f11 is not empty
        #     # f11 is very bad.
        #     result = f01.get_value() + f10.get_value() + f11.get_value()


        #return result

    def count_stones_edge_vertical(self, c):
        row = 0
        count1 = 0

        if not self.board_matrix[0][c].is_empty():
            player1 = self.board_matrix[0][c].player
            count1 = 1
            row = 1

            while row < Constants.BOARD_SIZE:
                if self.board_matrix[row][c].player == player1:
                    count1 += 1
                    row += 1
                else:
                    break

        if row == Constants.BOARD_SIZE:
            return count1
            # VOOR WIT OF ZWART GOED OF SLECHT ???

        row = Constants.BOARD_SIZE - 1
        count2 = 0

        if not self.board_matrix[row][c].is_empty():
            player2 = self.board_matrix[row][c].player
            count2 = 1
            row -= 1

            while row > 0:
                if self.board_matrix[row][c].player == player2:
                    count2 += 1
                    row -= 1
                else:
                    break

        print("VOOR WIE GUNSTIG??")
        return (count1 - count2) * Constants.UNFLIPABLE

    def count_stones_edge_horizontal(self, c):
        print("count_stones_edge_horizontal nog implementeren " + c)
        return 0

    def debug_show(self, board_matrix=None):
        if board_matrix is None:
            board_matrix = self.board_matrix

        for r in range(0, Constants.BOARD_SIZE):
            for c in range(0, Constants.BOARD_SIZE):
                if board_matrix[r][c].player is None:
                    print("  N   ", end="")
                else:
                    print(f"{board_matrix[r][c].player.color} ", end="")
            print("")

    def __eq__(self, b_matrix):
        for r in range(0, Constants.BOARD_SIZE):
            for c in range(0, Constants.BOARD_SIZE):
                if not self.board_matrix[r][c] == b_matrix[r][c]:
                    return False

        return True
