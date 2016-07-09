import Board

b = Board.Board()
#Qe5
b.setUp('8/8/8/6pP/6pK/8/8/8 w - - 0 1')

print b
print b.attackRange('white')

