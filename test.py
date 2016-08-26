#import Game
import Board

if __name__ == '__main__':
    g = Board.Board()
    g.move('e4')
    g.move('d5')
    g.move('exd5')
    g.move('e6')
    g.move('dxe6')
    g.move('Nf6')
    g.move('e7')
    g.move('Rg8')
    g.move('exd8')
    print g.__repr__
