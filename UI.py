import os
import Tkinter as tk
from PIL import ImageTk, Image
import sys
import Board

class Piece:
    rpath = r'pieces'
    def __init__(self, canvas, x, y, p, color):
        s = int(canvas['width'])/16
        opp = 'white' if color == 'black' else 'black'
        path = os.path.join(os.path.dirname(__file__), \
            Piece.rpath, color+p+'.png')

        self.canvas = canvas
        self.color = color
        self.p = p
        self.photo = ImageTk.PhotoImage(file=path)
        self.piece = canvas.create_image(x, y, image=self.photo)
        self.coord = (x,y)

    def move(self, dx, dy):
        #dx, dy are in pixels
        self.canvas.move(self.piece, dx, dy)
        self.coord = (self.coord[0]+dx, self.coord[1]+dy)
        
    def moveTo(self, x, y, square):
        #x, y are UI coord
        xpixel = y*square
        ypixel = x*square
        self.move(xpixel-self.coord[0]+square/2, ypixel-self.coord[1]+square/2)
    
    def __del__(self):
            self.canvas.delete(self.piece)

    def __repr__(self):
        return self.color + ' ' +self.p+' @ '+str(self.coord)

class BoardUI(tk.Tk):

    def __init__(self, square):
        tk.Tk.__init__(self)
        self.f = tk.Frame(self, height=square*8, width=square*8)
#        self.f.pack()

        self.pieces = [[None for _ in range(8)] for _ in range(8)]
        self.side = 8 * square
        self.offset = square / 2
        self.square = square

        self.canvas = tk.Canvas(self, width=self.side, height=self.side)
        self.canvas.pack()
        for x in range(8):
            for y in range(8):
                c = 'white' if (x+y)%2==0 else 'gray50'
                self.canvas.create_rectangle(x*square,y*square,\
                    x*square+square,y*square+square, fill=c)

    def setUp(self, d):
        self.pieces = [[None for _ in range(8)] for _ in range(8)]
        for x in range(8):
            for y in range(8):
                if d[x][y][1] == 'None':
                    continue
                else:
                    xPixel = self.offset + y*self.square
                    yPixel = self.offset + x*self.square
                    self.pieces[x][y] = Piece(self.canvas, xPixel, yPixel, \
                        d[x][y][0], d[x][y][1])
    
    def Update(self):
        self.f.update()

    def move(self, movetup):
        print self.pieces
        #movetup = ('O-O'/'O-O-O', 'white'/'black')
        # or 
        #movetup = (piece, start, end, taken)
        if movetup[0] == 'O-O': 
            if movetup[1] == 'white':
                temp = 7
            else:
                temp = 0

            #self.pieces takes board coords
            self.pieces[temp][4].moveTo(temp,6,self.square)
            self.pieces[temp][7].moveTo(temp,5,self.square)
            self.pieces[temp][6] = self.pieces[temp][4]
            self.pieces[temp][5] = self.pieces[temp][7]
            self.pieces[temp][4] = None
            self.pieces[temp][7] = None

        elif movetup[0] == 'O-O-O':
            if movetup[1] == 'white':
                temp = 7
            else:
                temp = 0

            self.pieces[temp][4].moveTo(temp,2,self.square)
            self.pieces[temp][0].moveTo(temp,3,self.square)
            self.pieces[temp][3] = self.pieces[temp][0]
            self.pieces[temp][2] = self.pieces[temp][4]
            self.pieces[temp][0] = None
            self.pieces[temp][4] = None

        else:
            startx, starty = Board.atb(movetup[1])
            endx, endy = Board.atb(movetup[2])
            
            #if taking a piece, remove it from the board
            if self.pieces[endx][endy] != None:
                del self.pieces[endx][endy]

            p = self.pieces[startx][starty]

            uicoordx, uicoordy = btu(endx, endy)
            p.moveTo(endx, endy, self.square)
            
            self.pieces[endx][endy] = self.pieces[startx][starty]
            self.pieces[startx][starty] = None
            
            #if taken != false
            #i.e. en. passant
            if movetup[3] != False:
                x,y = atu(movetup[3])
                del self.pieces[x][y]
            



def btu(x,y):
    #board coord to ui coord
    return (y,x)

def utb(x,y):
    #ui coord to board coord
    return (y,x)

def atu(move):
    #algebraic notation to ui coord
    x = Board.atb(move)
    return btu(x[0], x[1])

if __name__ == '__main__':
    #side is side of small square 
    side = 68
    b = Board.Board()
    ui = BoardUI(side)

    ui.setUp(b.board)
    tk.update()

