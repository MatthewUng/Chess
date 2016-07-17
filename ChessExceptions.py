
class ChessException(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return "A chess error has occurred"


class InvalidMoveException(ChessException):
    def __init__(self, string):
        self.string = string

    def __str__(self):
        return "Invalid Move: " + self.string
        
class AmbiguousMoveException(ChessException):
    def __init__(self, string):
        self.string = string

    def __str__(self):
        return "Ambigous Move: " + self.string

