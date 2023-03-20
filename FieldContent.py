class FieldContent:
    def __init__(self, player=None):
        # class Player
        self.player = player
        self.value = 0

    def is_empty(self):
        return self.player is None

    def place_stone(self, player):
        self.player = player

    def is_occupied_by(self, player):
        return self.player == player

    def contains_player1(self):
        return self.player.is_player1()

    def contains_player2(self):
        return self.player.is_player2()

    def set_value(self, value):
        self.value = value

    def get_value(self):
        if self.is_empty():
            return 0

        return self.contains_player1() if self.value else -self.value

    def __str__(self):
        return "Field_content: {self.player.__str__()}"

    def __eq__(self, f_content):
       print(self.player, f_content.player)
       return self.player == f_content.player
