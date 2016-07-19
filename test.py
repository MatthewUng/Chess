import Board
import Game

b = Board.Board()

f = open('sampleGame.txt')
for _ in range(32):
    try:
        line = f.readline()
        l = line.split()
        b.move(l[1])
        b.move(l[2])
    except:
#        print b.__repr__
        print l[0], l[1], l[2]
        print 'exception occurred'
        exit(1)

print b.__repr__
print l[0], l[1], l[2]
exit(1)

