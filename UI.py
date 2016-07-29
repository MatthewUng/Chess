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
        self.photo = ImageTk.PhotoImage(file=path)
        self.piece = canvas.create_image(x, y, image=self.photo)
        self.coord = (x,y)

    def move(self, dx, dy):
        self.canvas.move(self.piece, dx, dy)
        
    def moveTo(self, x, y):
        self.canvas.move

class BoardUI(tk.Tk):

    def __init__(self, square):
        tk.Tk.__init__(self)
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
        for x in range(8):
            for y in range(8):
                if d[x][y][1] == 'None':
                    continue
                else:
                    xPixel = self.offset + y*self.square
                    yPixel = self.offset + x*self.square
                    self.pieces[x][y] = Piece(self.canvas, xPixel, yPixel, \
                        d[x][y][0], d[x][y][1])
    
    def move(movetup):
        #movetup = ('O-O'/'O-O-O', 'white'/'black')
        # or 
        #movetup = (piece, start, end, taken)
        if movetup[0] == 'O-O' or movetup[0] == 'O-O-O':

        else:
            startx, starty = atu(movetup[1])
            endx, endy = atu(movetup[2])
            p = self.pieces[startx][starty]
            p.moveTo(endx, endy)
            if movetup[3] != False:
                #remove piece here
                pass



    #not sure this is needed
    def run(self):
        tk.mainloop()

def btu(x,y):
    #board coord to ui coord
    return (y,x)

def utb(x,y):
    #ui coord to board coord
    return (y,x)

def atu(move):
    #algebraic notation to ui coord
    x = Board.atb(move)
    return bta(x[0], x[1])

if __name__ == '__main__':
    #side is side of small square 
    side = 68
    b = Board.Board()
    ui = BoardUI(side)

    ui.setUp(b.board)
    ui.run()


