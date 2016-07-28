import os
from Tkinter import *
from PIL import ImageTk, Image

class piece:
    rpath = r'pieces'
    def __init__(self, canvas, x, y, p, color):
        s = int(canvas['width'])/16
        opp = 'white' if color == 'black' else 'black'
        path = os.path.join(os.path.dirname(__file__), \
            piece.rpath, color+p+'.png')

        self.canvas = canvas
        self.color = color
        self.photo = ImageTk.PhotoImage(file=path)
        self.piece = canvas.create_image(x, y, image=self.photo)

    def move(self, dx, dy):
        self.canvas.move(self.piece, dx, dy)
        

def createBoard(canvas, side):
    for x in range(8):
        for y in range(8):
            s = side/8
            c = 'white' if (x+y)%2==0 else 'gray50'
            canvas.create_rectangle(x*s,y*s,\
                x*s+s,y*s+s, fill=c)


def setUp(canvas,side):
    #length of square
    ss = side/8
    #half length of square
    s = ss/2

if __name__ == '__main__':
    square = 68
    offset = square / 2
    side = square * 8 
    root = Tk()
    w = Canvas(root, width=side, height=side)
    w.pack()
    

    createBoard(w,side)
    p = piece(w, offset, offset,'R','white')
    p.move(square, square)

    setUp(w,side)



    mainloop()
