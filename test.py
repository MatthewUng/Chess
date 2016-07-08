import Board

b = Board.Board()

print b

b.move('e4')
b.move('e5')

print Board.atb('f8')
print Board.atb('c5')

b.move('Bc4')
b.move('Bc5')

print b

b.move('Qf3')
b.move('Qf6')

print b
