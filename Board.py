
import re
import ChessExceptions

class Board:
    pieces = ['P','R','N','B','Q','K']
    initLoc = [['a','h',],['b','g'],\
               ['c','f'],['d'],['e']]
    NoPiece = (' ','None')
    stPattern = re.compile('([PRBNQK]{1})([a-h]{1}[1-8]{1})')
    resPattern = re.compile(
    '([PRBNQK]{1})([a-h]{,1}[1-8]{,1})([a-h]{1}[1-8]{1})')

    def __init__(self):
        self.ep = list()
        self.pLocW = dict()
        self.pLocB = dict()
        self.movelist = list()
        self.castleKW, self.castleKB = True, True
        self.castleQW, self.castleQB = True, True
        self.moves = 0
        self.turn = 'white'
        self.halfmoves = 0
        self.newGame()

    def reset(self):
        """Resets the Board to blank"""
        self.ep = list()
        self.movelist = list()
        self.board = [[Board.NoPiece for _ in range(8)] for _ in range(8)]

        #resetting piece dict
        for piece in Board.pieces:
            self.pLocW[piece] = set()
            self.pLocB[piece] = set()

    def newGame(self):
        """sets the board to a new game"""
        self.reset()
        self.castleKW, self.castleKB = True, True
        self.castleQW, self.castleQB = True, True
        self.moves = 0
        self.turn = 'white'
        self.halfmoves = 0
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
            self.pLocW['P'] |= set([chr(97+i)+'2'])
            self.pLocB['P'] |= set([chr(97+i)+'7'])
    
    def setUp(self, fen):
        """sets up the board based on FEN"""
        self.reset()
        spacesplit = fen.split(' ')
        p = spacesplit[0].split('/')
        x,y = 0,0
        for row in p:
            y = 0
            for piece in row:
                if ord(piece) >= 48 and ord(piece) <= 56:
                    for _ in range(int(piece)):
                        self.board[x][y] = Board.NoPiece
                        y += 1
                #white piece
                elif piece.isupper():
                    self.board[x][y] = (piece.upper(), 'white')
                    self.pLocW[piece.upper()] |= set([bta(x,y)])
                    y += 1

                #black piece
                elif piece.islower():
                    self.board[x][y] = (piece.upper(), 'black')
                    self.pLocB[piece.upper()] |= set([bta(x,y)])
                    y += 1

            #increment row var
            x += 1
        self.turn = 'white' if spacesplit[1] == 'w' else 'black'
        
        #setting castle vars
        castle = spacesplit[2]
        self.castleKW = True if 'K' in castle else False
        self.castleQW = True if 'Q' in castle else False
        self.castleKB = True if 'k' in castle else False
        self.castleQB = True if 'q' in castle else False

        #setting ep variables
        for i in range(0,len(spacesplit[3]),2):
            self.ep.append(spacesplit[3][i:i+2])
        if self.ep[0] == '-':
            self.ep.remove('-')
       
        self.halfmoves = int(spacesplit[4])
        self.moves = int(spacesplit[5]) - 1

    def update(self):
        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"
        self.moves += 1
    
    def parseMove(self, Input):
        """Checks semantics of move input"""
        move = Input.replace('x','')
        move = move.rstrip('+')
        if move[0].islower():
            move = 'P'+move
        if len(move) == 3:
            m = re.match(Board.stPattern, move)
            if m == None:
                return False
            return (m.group(1), m.group(2), '')
        elif len(move) > 3:
            m = re.match(Board.resPattern, move)
            if m == None:
                return False
            return (m.group(1), m.group(3), m.group(2))
        else:
            return False


    def move(self, move):
        """makes a certain move"""

        piecedict = self.pLocW if self.turn == 'white' else self.pLocB
        oppdict = self.pLocB  if self.turn == 'white' else self.pLocW
        opp = 'white' if self.turn == 'black' else 'black'
        taken = False

        if move == "O-O" or move == "O-O-O":
            if self.validCastle(move, self.turn):
                t = 7 if self.turn == 'white' else 0
                if move == "O-O":
                    self.board[t][6] = self.board[t][4]
                    self.board[t][4] = Board.NoPiece
                    piecedict['K'].pop()
                    self.board[t][5] = self.board[t][7]
                    self.board[t][7] = Board.NoPiece
                    if self.turn == 'white':
                        piecedict['K'].add('g1')
                        piecedict['R'].remove('h1')
                        piecedict['R'].add('f1')
                        self.castleKW = False
                        self.castleQW = False
                    else:
                        piecedict['K'].add('g8')
                        piecedict['R'].remove('h8')
                        piecedict['R'].add('f8')
                        self.castleKB = False
                        self.castleQB = False


                    self.movelist.append(move)

                elif move == "O-O-O":
                    self.board[t][2] = self.board[t][4]
                    self.board[t][4] = Board.NoPiece
                    piecedict['K'].pop()
                    self.board[t][3] = self.board[t][0]
                    self.board[t][0] = Board.NoPiece
                    if self.turn == 'white':
                        piecedict['K'].add('c1')
                        piecedict['R'].remove('a1')
                        piecedict['R'].add('f1')
                        self.castleKW = False
                        self.castleQW = False

                    else:
                        piecedict['K'].add('c8')
                        piecedict['R'].remove('a8')
                        piecedict['R'].add('f8')
                        self.castleKB = False
                        self.castleQB = False

                    self.movelist.append(move)
                
                temp = self.turn
                self.update()
                return (move, temp)
            else:
                raise ChessExceptions.ChessException

        #move is normal
        else:
            move = self.parseMove(move)

            #error
            if not move:
                raise ChessExceptions.InvalidMoveException(move)

            #move is fine
            piece = move[0]
            end = move[1]
            r = move[2]

        possPieces = piecedict[piece]
        
        if r:
            possPieces = filter(lambda x: r in x, possPieces)

            if len(possPieces) == 0:
                raise ChessExceptions.InvalidMoveException(move)

        moves = filter(lambda x: self.validMove(piece, x, end),\
          possPieces)

        if len(moves) != 1:
            raise ChessExceptions.AmbiguousMoveException(move[0]+move[1])
        
        if self.moveCheck(piece, moves[0],end, self.turn):
            #move puts king under check
            raise ChessExceptions.InvalidMoveException(move)

        #move valid
        #make move
        else:
            #end is location to move to
            #moves[0] is the starting loc
            x,y = atb(end)
            X,Y = atb(moves[0])
            #if piece is taken
            #need to remove it from dict
            if self.board[x][y][1] == opp:
                oppdict[self.board[x][y][0]].remove(end)
            self.board[x][y] = (piece, self.turn)
            self.board[X][Y] = Board.NoPiece
            piecedict[piece].remove(moves[0])
            piecedict[piece].add(end) 

            

            if end not in self.ep:
                del self.ep[:]

            #ep case
            if piece == 'P':
                #promotion
                if x == 0 or x == 7:
                    if move[-1] in Board.pieces and\
                    move[-1] != 'P':
                        ppiece = move[-1]
                        self.board[x][y] = (ppiece,self.turn)
                    else:
                        ppiece = raw_input('Pick a piece to promote to: ')
                        while ppiece not in Board.pieces or\
                        ppiece == 'P':
                            ppiece = raw_input('Pick a piece to promote to: ')
                        self.board[x][y] = (ppiece, self.turn)
                        move += ppiece
                    piecedict['P'].remove(end)
                    piecedict[ppiece].add(end)

                #adding to ep list
                start = 6 if self.turn == 'white' else 1
                t = -2 if self.turn == 'white' else 2
                if abs(x-X) == 2 and X == start:
                    self.ep.append(bta(X+t/2,y))
                #removing pawn from board
                elif end in self.ep:
                    t = 1 if self.turn == 'white' else -1
                    self.board[x+t][y] = Board.NoPiece
                    oppdict = self.pLocB if self.turn == 'white'\
                      else self.pLocW
                    oppdict['P'].remove(bta(x+t,y))
                    del self.ep[:]
                   
            #setting castling variables
            if self.turn == 'white': 
                if piece == 'R':
                    if moves[0] == 'a1':
                        self.castleQW = False
                    elif moves[0] == 'h1':
                        self.castleKW = False
                elif piece == 'K':
                    if moves [0] == 'e1':
                        self.castleQW = False
                        self.castleKW = False
            elif self.turn == 'black':
                if piece == 'R':
                    if moves[0] == 'a8':
                        self.castleQB = False
                    elif moves[0] == 'h8':
                        self.castleKB = False
                if piece == 'K':
                    if moves[0] == 'e8':
                        self.castleQB = False
                        self.castleKB = False
            
            #if game is over
            if self.mateCheck(opp):
                raise ChessExceptions.checkMateException(self.turn)

            self.update()
            self.movelist.append(move)
            return (piece, moves[0], end, taken)

    def validCastle(self, move, side):
        """determines if castling is valid"""
        if side == "white":
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
                    
        elif side == "black":
          
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
                if self.castleKB == False:
                    return False
                for index in [5,6]:
                    if self.board[0][index][1] != "None":
                        return False
                for square in ['f8','g8']:
                    if square in self.attackRange('white'):
                        return False
                return True           
        return False

    def getCastling(self, side):
        """returns possible castling moves"""
        out = list()
        for i in ['O-O', 'O-O-O']:
            if self.validCastle(i, side):
                out.append(i)
        return out 

    def getMoves(self, side):
        d = self.pLocW if side == 'white' else self.pLocB
        def fileCheck(start):
            """possible moves of file pieces"""
            x,y = atb(start)
            out = set()
            for i in range(1,8-y):
                if self.board[x][y+i][1] != 'None':
                    if self.board[x][y+i][1] != side:
                        out |= set([bta(x,y+i)])
                    break
                else:
                    out |= set([bta(x,y+i)])

            for i in range(1,y+1):
                if self.board[x][y-i][1] != 'None':
                    if self.board[x][y-i][1] != side:
                        out |= set([bta(x,y-i)])
                    break
                else:
                    out |= set([bta(x,y-i)])

            for i in range(1,8-x):
                if self.board[x+i][y][1] != 'None':
                    if self.board[x+i][y][1] != side:
                        out |= set([bta(x+i,y)])
                    break
                else:
                    out |= set([bta(x+i,y)])

            for i in range(1,x+1):
                if self.board[x-i][y][1] != 'None':
                    if self.board[x-i][y][1] != side:
                        out |= set([bta(x-i,y)])
                    break
                else:
                    out |= set([bta(x-i,y)])
            return out
        
        def diagCheck(start):
            """possible moves with the Bishop"""
            x,y = atb(start)
            out = set()

            #upper right diag
            
            for i in range(1, min(x+1, 8-y)):
                if self.board[x-i][y+i][1] != 'None':
                    if self.board[x-i][y+i][1] != side:
                        out |= set([bta(x-i,y+i)])
                    break
                else:
                    out |= set([bta(x-i,y+i)])

            #upper left diag 
            for i in range(1, min(x+1, y+1)):
                if self.board[x-i][y-i][1] != 'None':
                    if self.board[x-i][y-i][1] != side:
                        out |= set([bta(x-i,y-i)])
                    break
                else:
                    out |= set([bta(x-i,y-i)])

            #lower right diag
            for i in range(1, min(8-x, 8-y)):
                if self.board[x+i][y+i][1] != 'None':
                    if self.board[x+i][y+i][1] != side:
                        out |= set([bta(x+i,y+i)])
                    break
                else:
                    out |= set([bta(x+i,y+i)])

            #lower left diag
            for i in range(1, min(8-x, y+1)):
                if self.board[x+i][y-i][1] != 'None':
                    if self.board[x+i][y-i][1] != side:
                        out |= set([bta(x+i,y-i)])
                    break
                else:
                    out |= set([bta(x+i,y-i)])
            return out

        def knightCheck(start):
            """possible moves with the knight"""
            x,y = atb(start)
            potential = list()
            for i in [1,-1]:
                for j in [-2,2]:
                    potential.append((x+i,y+j))
            for i in [-2,2]:
                for j in [-1,1]:
                    potential.append((x+i,y+j))
            for tup in potential[:]:
                if min(tup) < 0 or max(tup) > 7:
                    potential.remove(tup)
                elif self.board[tup[0]][tup[1]][1] == self.board[x][y][1]:
                    potential.remove(tup)
            return set(map(lambda tup: bta(tup[0],tup[1]), potential))

        def kingCheck(start):
            """possible moves with the king"""
            x,y = atb(start)
            potential = list()
            for i in [-1,0,1]:
                for j in [-1,0,1]:
                    if i == j and j == 0:
                        continue
                    else:
                        potential.append((x+i,y+j))  
            for tup in potential[:]:
                if min(tup) < 0 or max(tup) > 7:
                    potential.remove(tup)
                elif self.board[tup[0]][tup[1]][1] == self.board[x][y][1]:
                    potential.remove(tup)
            return set(map(lambda tup: bta(tup[0],tup[1]),potential))
            
        def pawnCheck(start):
            """possible moves with pawn"""
            out = list()
            x,y = atb(start)
            t = -1 if side == 'white' else 1
            start = 6 if side == 'white' else 1
            opp = 'black' if side == 'white' else 'white'

            if self.board[x+t][y] == Board.NoPiece:
                out.append(bta(x+t,y))
                if x == start and self.board[x+2*t][y] == Board.NoPiece:
                    out.append(bta(x+2*t,y))
            for Y in [-1, 1]:
                if min(x+t, y+Y) >=0 and max(x+t,y+Y) <=7:
                    if self.board[x+t][y+Y][1] == opp:
                        out.append(bta(x+t,y+Y))
            return out

        #start of function
        out = list()
        for piece, loc in d.items():
            if piece == 'R' or piece == 'Q':
                for l in loc:
                    for end in fileCheck(l):
                        out.append((piece, l, end))
            if piece == 'B' or piece == 'Q':
                for l in loc:
                    for end in diagCheck(l):
                        out.append((piece, l, end))
            elif piece == 'N':
                for l in loc:
                    for end in knightCheck(l):
                        out.append((piece, l, end))
            elif piece == 'K':
                for l in loc:
                    for end in kingCheck(l):
                        out.append((piece, l, end))
            elif piece == 'P':
                for l in loc:
                    for end in pawnCheck(l):
                        out.append((piece, l, end))
        return out

    def checkCheck(self, side):
        """checks if the side is in check or not"""
        opp = 'black' if side == 'white' else 'white'
        d = self.pLocW if side == 'white' else self.pLocB
        if list(d['K'])[0] in self.attackRange(opp):
            return True
        else: 
            return False
           
    def attackRange(self, side):
        """determines the squares that a certain side is attacking"""

        def fileCheck(start):
            """attackRange of file pieces"""
            x,y = atb(start)
            out = set()
            for i in range(1,8-y):
                if self.board[x][y+i][1] != 'None':
                    if self.board[x][y+i][1] != side:
                        out |= set([bta(x,y+i)])
                    break
                else:
                    out |= set([bta(x,y+i)])

            for i in range(1,y+1):
                if self.board[x][y-i][1] != 'None':
                    if self.board[x][y-i][1] != side:
                        out |= set([bta(x,y-i)])
                    break
                else:
                    out |= set([bta(x,y-i)])

            for i in range(1,8-x):
                if self.board[x+i][y][1] != 'None':
                    if self.board[x+i][y][1] != side:
                        out |= set([bta(x+i,y)])
                    break
                else:
                    out |= set([bta(x+i,y)])

            for i in range(1,x+1):
                if self.board[x-i][y][1] != 'None':
                    if self.board[x-i][y][1] != side:
                        out |= set([bta(x-i,y)])
                    break
                else:
                    out |= set([bta(x-i,y)])
            return out
        
        def diagCheck(start):
            """attack range of diag pieces""" 
            x,y = atb(start)
            out = set()

            #upper right diag
            
            for i in range(1, min(x+1, 8-y)):
                if self.board[x-i][y+i][1] != 'None':
                    if self.board[x-i][y+i][1] != side:
                        out |= set([bta(x-i,y+i)])
                    break
                else:
                    out |= set([bta(x-i,y+i)])

            #upper left diag 
            for i in range(1, min(x+1, y+1)):
                if self.board[x-i][y-i][1] != 'None':
                    if self.board[x-i][y-i][1] != side:
                        out |= set([bta(x-i,y-i)])
                    break
                else:
                    out |= set([bta(x-i,y-i)])

            #lower right diag
            for i in range(1, min(8-x, 8-y)):
                if self.board[x+i][y+i][1] != 'None':
                    if self.board[x+i][y+i][1] != side:
                        out |= set([bta(x+i,y+i)])
                    break
                else:
                    out |= set([bta(x+i,y+i)])

            #lower left diag
            for i in range(1, min(8-x, y+1)):
                if self.board[x+i][y-i][1] != 'None':
                    if self.board[x+i][y-i][1] != side:
                        out |= set([bta(x+i,y-i)])
                    break
                else:
                    out |= set([bta(x+i,y-i)])
            return out

        def knightCheck(start):
            """attack range of knight"""
            x,y = atb(start)
            potential = list()
            for i in [1,-1]:
                for j in [-2,2]:
                    potential.append((x+i,y+j))
            for i in [-2,2]:
                for j in [-1,1]:
                    potential.append((x+i,y+j))
            for tup in potential[:]:
                if min(tup) < 0 or max(tup) > 7:
                    potential.remove(tup)
                elif self.board[tup[0]][tup[1]][1] == self.board[x][y][1]:
                    potential.remove(tup)
            return set(map(lambda tup: bta(tup[0],tup[1]), potential))

        def kingCheck(start):
            """attack range of the king"""
            x,y = atb(start)
            potential = list()
            for i in [-1,0,1]:
                for j in [-1,0,1]:
                    if i == j and j == 0:
                        continue
                    else:
                        potential.append((x+i,y+j))  
            for tup in potential[:]:
                if min(tup) < 0 or max(tup) > 7:
                    potential.remove(tup)
                elif self.board[tup[0]][tup[1]][1] == self.board[x][y][1]:
                    potential.remove(tup)
            return set(map(lambda tup: bta(tup[0],tup[1]),potential))
            
        def pawnCheck(start,side):
            """attack range of the pawn"""
            x,y = atb(start)
            t = -1 if side == 'white' else 1
            potential = list()
            for i in [-1,1]:
                potential.append((x+t, y+i))

            for tup in potential[:]:
                if min(tup) < 0 or max(tup) > 7:
                    potential.remove(tup)
                elif self.board[tup[0]][tup[1]][1] == self.board[x][y][1]:
                    potential.remove(tup)
            return set(map(lambda tup: bta(tup[0],tup[1]),potential))
            

        out = set()
        p = self.pLocW if side == "white" else self.pLocB
        
        for piece, locSet in p.items():
            if bool(locSet):
                if piece == 'Q':
                    for loc in locSet:
                        out |= diagCheck(loc)
                        out |= fileCheck(loc)
                if piece == 'R':
                    for loc in locSet:
                        out |= fileCheck(loc)
                if piece == 'B':
                    for loc in locSet:
                        out |= diagCheck(loc)
                if piece == 'N':
                    for loc in locSet:
                        out |= knightCheck(loc)
                if piece == 'K':
                    for loc in locSet:
                        out |= kingCheck(loc)
                if piece == 'P':
                    for loc in locSet:
                        out |= pawnCheck(loc,side)
        return out

    def validMove(self, piece, start, end):
        """determines if a move is valid for that piece"""
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
                for i in range(min(x,X)+1, max(x,X)):
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
                opp = 'black' if self.board[x][y][1] == 'white' else 'white'
                if end not in self.attackRange(opp):
                    return True
            else:
                return False

        #Queen
        elif piece == 'Q':
            return fileCheck(x,y,X,Y) or diagCheck(x,y,X,Y)
        
        elif piece == "P":
            #t = turn
            t = 1
            if self.turn == 'white':
                t = -1
            opp = 'white' if self.turn == 'black' else 'black'

            #pawn moves forward one
            if x + t == X and y == Y and self.board[X][Y] == Board.NoPiece:
                return True

            #taking pieces
            elif x+t == X and abs(y-Y) == 1 and self.board[X][Y][1] == opp:
                return True
            
            #moving two steps forward
            elif ((x == 6 and self.turn == 'white' and X==4 ) \
              or (x == 1 and self.turn == 'black' and X == 3)) and y == Y \
              and self.board[x+t][y] == Board.NoPiece:

                return True

            #ep
            elif end in self.ep and x + t == X and abs(y-Y) == 1:
                return True
            else:
                return False

    def moveCheck(self, piece, start, end, side):
        """checks if a move doesn't put the king under check"""
        x,y = atb(start)
        X,Y = atb(end)
        out = False

        #setting variables
        opp = 'black' if side == 'white' else 'white'
        d = self.pLocB if opp == 'white' else self.pLocW
        oppd = self.pLocW if opp == 'white' else self.pLocB
        old = self.board[X][Y]
        
        #altering board
        self.board[X][Y] = self.board[x][y]
        self.board[x][y] = Board.NoPiece
        
        
        if old != Board.NoPiece:
            oppd[old[0]].remove(end)
        d[piece].remove(start)
        d[piece].add(end)
       
        #check if king still in check 
        if list(d['K'])[0] in self.attackRange(opp):
            out = True
        
        #putting board back together
        self.board[x][y] = self.board[X][Y]
        self.board[X][Y] = old

        if old != Board.NoPiece:
            oppd[old[0]].add(end)
        d[piece].add(start)
        d[piece].remove(end)

        return out 

    def mateCheck(self, side):
        """determines if a certain side is checkmated"""
        if self.checkCheck(side):
            for move in self.getMoves(side):
                if not self.moveCheck(move[0],move[1],move[2],side):
                    #if move does not induce check
                    #it is not checkmate
                    return False


            #if there is a valid castling move, 
            #it is not checkmate
            for move in self.getCastling(side):
                return False 
            return True
        else:
            return False

    def getD(self):
        return self.board

    def __getitem__(self, key):
        x,y = list(key)
        return self.board[8-int(y)][ord(x)-97]

    def __setitem__(self, key, value):
        x,y = list(key)
        self.board[8-int(y)][ord(x)-97] = value

    def __repr__(self):
        out = list()
        #adding self.board
        for line in self.board:
            for square in line:
                out.append(str(square))
        b = '\n' + ("{:<15} " * 8 + '\n') * 8 
        out = b.format(*out) 

        #adding pieceloc dict
        out += '\n\nWhite piece loc Dict: \n'
        for piece, loc in self.pLocW.items():
            out += "{} : {}\n".format(piece,loc)

        out += '\nBlack piece loc Dict: \n'
        for piece, loc in self.pLocB.items():
            out += "{} : {}\n".format(piece, loc)
        
        #adding ep list
        out += "\nEP list: \n"
        out += str(self.ep) + '\n'

        #adding castling rights
        out += "\nWhite can still castle: "
        if self.castleKW == True: 
            out += "Kingside "
        if self.castleQW == True:
            out += "Queenside"
        out += '\n'
        out += "Black can still castle: "
        if self.castleKB == True:
            out += "Kingside "
        if self.castleQB == True:
            out += "Queenside"
        out += '\n\n'


        #adding moves

        out += "There has been {} moves:\n".format(self.moves)
        if len(self.movelist) % 2 == 0:
            if len(self.movelist) == 0:
                pass
            else:
                for i in range((self.moves)/2):
                    out += "{}. {:<5} {:<5}\n".format(i+1, \
                      self.movelist[2*i],self.movelist[1+2*i])
        else:
            for i in range((self.moves-1)/2):
                out += "{}. {:<5} {:<5}\n".format(i+1, \
                  self.movelist[2*i],self.movelist[1+2*i])
            out += "{}. {:<5}\n".format(self.moves/2+1, self.movelist[-1])

        out += "\nThere have been {} halfmoves made.\n".format(self.halfmoves)+\
          "It is currently {} to move.\n".format(self.turn)
        return '\n\n' + str(self) + out+'\n'     

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

