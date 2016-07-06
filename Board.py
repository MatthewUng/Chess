class Board:
    pieces = ['p','R','N','B','Q','K']
    initLoc = [['a','h',],['b','g'],\
               ['c','f'],['d'],['e']]
    ep = list()
    castleW, castleB = True, True
    pLocW = dict()
    plocB = dict()

    def __init__(self):
        for piece in pieces:
            pLoc[piece] = []
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
        move = move.rstrip('+')
        move = move.replace('x','')

        if not move[0].isupper():
            move = 'p'+move

        if move[0] not in pieces:
            return False

        if validmove(    

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
    """determines if a move is valid"""
    
    #lower -> start
    #upper -> end
    y,x = ord(start[0])-97, int(start[1]) - 1
    Y,X = ord(end[0])-97, int(end[1]) - 1

    def fileCheck(x,y,X,Y):
        if x == X:
            #can't have pieces between start and end
            for i in range(min(y,Y)+1,max(y,Y)):
                if self.board[x][i][1] != 'None':
                    return False
            return True
              
        #same logic as above
        elif y == Y:
            for i inrange(min(x,X), max(x,X)):
                if self.board[i][y][1] != 'None':
                    return False
            return True
        return False
    
    def diagCheck(x,y,X,Y):
        #positive slope
        if x-X == y-Y:
            for i in range(1, abs(X-x)):
                if self.board[min(x,X)+i][min(y,Y)+i][1] != 'None':
                    return False
                return True
        #negative slope
        elif x+X == y+Y:
            for i in range(1, abs(x-X)):
                if self.board(min(x,X)+i][max(y,Y)-i][1] != 'None':
                    return False
            return True
       return False
    
    #endcheck
    if self.board[x][y][1] == self.board[X][Y][1]:
        return False

    #checking if values in range
    for i in [x,X,y,Y]:
        if i < 0 or i > 7:
            return False

    #Rook
    if piece == 'R':
        return fileCheck(x,y,X,Y)

    #Bishop
    elif piece == 'B':
        return diagCheck(x,y,X,Y)
    
    #Knight
    elif piece == "N":
        if abs(x-X)+abs(y-Y) == 3 and abs(x-X) > 0 and abs(x-X) < 0:
            return True
    
    #King
    elif piece == 'K':
        if abs(x-X) <= 1 and abs(y-Y) <= 1:
            return True

    #Queen
    elif piece == 'Q':
        return fileCheck(x,y,X,Y) or diagCheck(x,y,X,Y)
        
