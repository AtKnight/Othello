import Constants


class Player:
    def __init__(self, name):
        # None, Constants.PLAYER1, or Constants.PLAYER2

        self.name = name

        if self.name is None:
            self.color = None
        elif self.name is Constants.PLAYER1:
            self.color = Constants.COLOR_PLAYER1
        else:
            self.color = Constants.COLOR_PLAYER2

    def is_player1(self):
        return self.name is Constants.PLAYER1

    def is_player2(self):
        return self.name is Constants.PLAYER2

    def is_empty(self):
        return self.name is None

    def get_opponent(self):
        if self.is_player1():
            return Player(Constants.PLAYER2)
        else:
            return Player(Constants.PLAYER1)

    def __eq__(self, obj):
        return self.name == obj.name

    def __str__(self):
        return f"name={self.name} kleur={self.color}"
