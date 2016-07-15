import Board

b = Board.Board()
b.setUp('8/P7/8/3K4/5k2/8/5p2/8 w - - 0 1')

b.move('a8Q')
b.move('f1Q')
"""
b.move('e4')
b.move('e5')
b.move('Nf3')
b.move('Nc6')
b.move('Bc4')
"""

print b.__repr__

