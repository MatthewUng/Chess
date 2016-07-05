class Board:
    pieces = ['p','R','N','B','Q','K']
    initLoc = [['a','h',],['b','g'],\
               ['c','f'],['d'],['e']]
    def __init__(self):
        self.reset()

    def reset(self):
        self.board = [[(' ','None') for _ in range(8)] for _ in range(8)]

        # 1, 2, ... , len(pieces) - 1
        for i in range(1, len(Board.pieces)):
            for j in Board.initLoc[i-1]:
                self[j+'1'] = (Board.pieces[i],'white')
                self[j+'8'] = (Board.pieces[i], 'black')
        for i in range(8):
            self[chr(97+i)+'2'] = (Board.pieces[0],'white')
            self[chr(97+i)+'7'] = (Board.pieces[0],'black')

    def move(self, move):
        

    def __getitem__(self, key):
        x,y = list(key)
        return self.board[8-int(y)][ord(x)-97]

    def __setitem__(self, key, value):
        x,y = list(key)
        self.board[8-int(y)][ord(x)-97] = value

    def __repr__(self):
        out = list()
        for line in self.board:
            for square in line:
                out.append(str(square))
            out.append('\n')
        return ''.join(out)
            
    def __str__(self):
        out = list()
        for line in self.board:
            for piece in line:
                out.append(piece[0]+' ')
            out.append('\n')
        return ''.join(out)


def validMove(piece, start, end):
    x,y = ord(start[0])-97, int(start[1]) - 1
    X,Y = ord(end[0])-97, int(end[1]) - 1
    for i in [x,X,y,Y]:
        if i < 0 or i > 7:
            return False

    if piece == 'R':
        if x == X or y == Y:
            return True
    elif piece = 'B':
        
