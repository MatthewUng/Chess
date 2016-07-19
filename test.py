import Board
import Game
import re

#pattern = re.compile(r'[\d]+\.\s(.+?)\s(.+?)\s')
b = Board.Board()

b.move('f4')
b.move('e5')
b.move('g4')
b.move('Qh4')

print b.checkCheck('white')
print 'middle'
print b.mateCheck('white')

print b.__repr__
