import Bot
import Board
import time

if __name__ == '__main__':
    name = raw_input("input file containing fen: ")
    f = open(name, 'r')
    fen = f.read()
    b = Board.Board()
    b.setUp(fen)
    print '\n',b

    t = Bot.Tree(b, b.turn)
    print "Currently calculating..."
    start_time = time.time()
    move = t.minimax(3)
    end_time = time.time()
    if move[0][0][3] == None:
        s = move[0][0][0] + move[0][0][1] + move[0][0][2]
    else:
        s = reduce(lambda x,y: x+y, move[0])
    print "\n{} is the best calculated move with an evaluation of {}".format(s,move[1])
    print "{} total seconds to compute".format(end_time - start_time)
