import Board
import UI

class Game:
    def __init__(self):
        self.b = Board.Board()
        self.ui = UI.BoardUI(68)
        self.ui.setUp(self.b.getD())
        self.ui.update()

    def printBoard(self):
        print self.b
    
    def move(self, move):
        movetup = self.b.move(move)
        print movetup
        self.ui.move(movetup)
    
    def update(self):
        self.ui.Update()
    
def main():
    g = Game()
    try:
        while True:
            g.printBoard()
            print "It is {} to move.".format(g.b.turn)
            move = raw_input("Input a move: ")
            g.move(move)             
            g.update()

    except Exception as e:
        print e

if __name__ == "__main__":
    main()

