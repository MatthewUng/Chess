import Board

b = Board.Board()
#b.setUp('r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4')

b.move('e4')
b.move('e5')
b.move('Nf3')
b.move('Nc6')

print b.__repr__

