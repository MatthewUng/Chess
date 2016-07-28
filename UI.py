import os
from Tkinter import *
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
        


class BoardUI:

    def __init__(self, square):
        self. pieces = [[None for _ in range(8)] for _ in range(8)]
        self.side = 8 * square
        self.offset = square / 2
        self.square = square
        self.root = Tk()
        self.canvas = Canvas(self.root, width=self.side, height=self.side)
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
    def run(self):
        mainloop()

if __name__ == '__main__':
    #side is side of small square 
    side = 68
    b = Board.Board()
    ui = BoardUI(side)

    ui.setUp(b.board)
    ui.run()


