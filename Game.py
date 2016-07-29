import Board
import UI

class Game:
    def __init__(self):
        self.b = Board.Board()
        self.ui = UI.BoardUI()

    def printBoard(self):
        print self.b
    
    def move(self, move):
        movetup = self.b.move(move)
        self.ui.move(movetup)
        
    
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

