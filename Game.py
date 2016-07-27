import Board


class Game:
    def __init__(self):
        self.b = Board.Board()
        
    def printBoard(self):
        print self.b
    
    def move(self, move):
        self.b.move(move)
    
    
def main():
    g = Game()
    try:
        while True:
            g.printBoard()
            print "It is {} to move.".format(g.b.turn)
            move = raw_input("Input a move: ")
            g.move(move)             

    except Exception as e:
        print e

if __name__ == "__main__":
    main()

