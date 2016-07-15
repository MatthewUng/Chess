import Board

b = Board.Board()
#b.setUp('r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w Kq e4d5 4 4')


b.move('a4')
b.move('d5')
b.move('a5')
b.move('d4')
b.move('e4')
b.move('dxe3')

"""
b.move('d6')
b.move('Nf3')
b.move('Nc6')
b.move('Bc4')
b.move('Bg4')
b.move('O-O')
b.move('Qd7')
b.move('Kh1')
b.move('O-O-O')
"""

print b.__repr__

