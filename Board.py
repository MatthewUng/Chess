#TODO: IMPLEMENT EN PASSANT
#TODO: IMPLEMENT attackRange()
class Board:
    pieces = ['p','R','N','B','Q','K']
    initLoc = [['a','h',],['b','g'],\
               ['c','f'],['d'],['e']]
    NoPiece = (' ','None')

    def __init__(self):
        self.ep = list()
        self.castleKW, self.castleKB = True, True
        self.castleQW, self.castleQB = True, True
        self.pLocW = dict()
        self.pLocB = dict()
        self.moves = 1
        self.movelist = list()
        self.turn = 'white'
        self.reset()

    def reset(self):
        """Resets the Board"""
        self.board = [[Board.NoPiece for _ in range(8)] for _ in range(8)]

        #resetting piece dict
        for piece in Board.pieces:
            self.pLocW[piece] = set()
            self.pLocB[piece] = set()

        # 1, 2, ... , len(pieces) - 1
        for i in range(1, len(Board.pieces)):
            for j in Board.initLoc[i-1]:
                self[j+'1'] = (Board.pieces[i],'white')
                self[j+'8'] = (Board.pieces[i], 'black')
                self.pLocW[Board.pieces[i]] |= set([j+'1'])
                self.pLocB[Board.pieces[i]] |= set([j+'8'])
        for i in range(8):
            self[chr(97+i)+'2'] = (Board.pieces[0],'white')
            self[chr(97+i)+'7'] = (Board.pieces[0],'black')
            self.pLocW['p'] |= set([chr(97+i)+'2'])
            self.pLocB['p'] |= set([chr(97+i)+'7'])

    def update(self):
        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"
            self.moves += 1

    def move(self, move):
        """makes a certain move"""

        piecedict = self.pLocW if self.turn == 'white' else self.pLocB
        move = move.rstrip('+')
        move = move.replace('x','')
        
        if not move[0].isupper():
            move = 'p'+move

        #1st     char should designate piece
        piece = move[0]
        #last two char should be end loc
        loc = move[-2:]

        if move[0] not in Board.pieces:
            return False
       

        moves = filter(lambda x: self.validMove(piece, x, loc),\
          piecedict[piece])


        if len(moves) != 1:
            return False

        #move valid
        #make move
        else:
            #loc is location to move to
            #moves[0] is the starting loc
            x,y = atb(loc)
            X,Y = atb(moves[0])
            self.board[x][y] = (piece, self.turn)
            self.board[X][Y] = Board.NoPiece
            piecedict[piece].remove(moves[0])
            piecedict[piece] |= set([loc])

            if self.turn == 'black':
                self.moves += 1

            self.update()
            self.movelist.append(move)
        """
        self.castleKW, self.castleKB = True, True
        self.castleQW, self.castleQB = True, True
        """
    def validCastle(self, move):
        if self.turn == "white":
            #White Queenside Castle
            if move == "O-O-O":
                if self.castleQW == False:
                    return False
                for index in [1,2,3]:
                    if self.board[7][index][1] != "None":
                        return False
                for square in ['b1','c1','d1']:
                    if square in self.attackRange('black'):
                        return False
                return True
            
            #White Kingside Castle
            elif move == "O-O":
                if self.castleKW == False:
                    return False
                for index in [5,6]:
                    if self.board[7][index][1] != "None":
                        return False
                for square in ['f1','g1']:
                    if square in self.attackRange('black'):
                        return False
                return True           
                    
        elif self.turn == "black":
          
            #Black Queenside Castle
            if move == "O-O-O":
                if self.castleQB == False:
                    return False
                for index in [1,2,3]:
                    if self.board[0][index][1] != "None":
                        return False
                for square in ['b8','c8','d8']:
                    if square in self.attackRange('white'):
                        return False
                return True           

            #Black Kingside Castle
            elif move == "O-O":
                 if self.castleBW == False:
                    return False
                for index in [5,6]:
                    if self.board[0][index][1] != "None":
                        return False
                for square in ['f8','g8']:
                    if square in self.attackRange('white'):
                        return False
                return True           
           
    def attackRange(self, side):
        out = set()
        p = selfpLocW if side == "white" else self.pLocB
        
        for piece, loc in p.items():

    def validMove(self, piece, start, end):
        """determines if a move is valid"""
        
        #lower -> start
        #upper -> end
        x,y = atb(start)
        X,Y = atb(end)

        def fileCheck(x,y,X,Y):
            if x == X:
                #can't have pieces between start and end
                for i in range(min(y,Y)+1,max(y,Y)):
                    if self.board[x][i][1] != 'None':
                        return False
                return True
                  
            #same logic as above
            elif y == Y:
                for i in range(min(x,X), max(x,X)):
                    if self.board[i][y][1] != 'None':
                        return False
                return True
            return False
        
        def diagCheck(x,y,X,Y):

            #positive slope
            #x is decremented and y is incremented
            if x+y == X+Y:
                
                for i in range(1, abs(X-x)):
                    if self.board[max(x,X)-i][min(y,Y)+i][1] != 'None':
                        
                        return False
                return True

            #negative slope
            #x is incremented and y is incremenmted
            elif x-X == y-Y:
                for i in range(1, abs(x-X)):
                    if self.board[min(x,X)+i][min(y,Y)+i][1] != 'None':
                        return False
                return True
        
        #endcheck
        if self.board[x][y][1] == self.board[X][Y][1]:
            print "end loc taken"
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
            if abs(x-X)+abs(y-Y) == 3 and abs(x-X) > 0 and abs(x-X) < 3:
                return True
            else: 
                return False
        #King
        elif piece == 'K':
            if abs(x-X) <= 1 and abs(y-Y) <= 1:
                return True
            else:
                return False

        #Queen
        elif piece == 'Q':
            return fileCheck(x,y,X,Y) or diagCheck(x,y,X,Y)
        
        elif piece == "p":
            #t = turn
            t = 1
            if self.turn == 'white':
                t = -1
            opp = 'white' if self.turn == 'black' else 'black'

            #pawn moves forward one
            if x == t + X and y == Y and self.board[X][Y] == Board.NoPiece:
                return True

            #taking pieces
            elif x == t + X and abs(y-Y) == 1 and self.board[X][Y][1] == opp:
                return True
            
            #moving two steps forward
            elif ((x == 6 and self.turn == 'white' and X==4 ) \
              or (x == 1 and self.turn == 'black' and X == 3)) and y == Y \
              and self.board[x+t][y] == Board.NoPiece:

                return True

            #ep
            elif True:
                pass
            else:
                return False



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
    


        
def atb(alg):
    """algebraic notation to board notation"""
    x,y=list(alg)
    return (8-int(y),ord(x)-97)

def bta(x,y):
    """board notation to algebraic notation"""
    return chr(97+y)+str(8-x)

