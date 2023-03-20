BOARD_SIZE = 8

PLAYER1 = "player1"  # starts the game
PLAYER2 = "player2"
COLOR_PLAYER1 = "black"
COLOR_PLAYER2 = "white"

BACKGROUND_COLOR = "green"
SELECTABLE_COLOR = "pink"
MOVE_COLOR = "red"

FILENAME_PLAYED_MOVES = "playedMoves.txt"

UNFLIPABLE = 5
NORMAL_DEPTH = 2
END_STONES = 56

SHOW = True
SHOWNOT = False


# corner (0, 0) (0, 1) (0, 2) A B C
#        (1, 0) (1, 1) (1, 2) B D E
#        (2, 0) (2, 1) (2, 2) C E F

A = 10
B = -3
C = 2
D = -8
E = 1
F = 2

field_values = {(0, 0): A,
                (0, 1): B,
                (0, 2): C,
                (1, 0): B,
                (1, 1): D,
                (1, 2): E,
                (2, 0): C,
                (2, 1): E,
                (2, 2): F}
