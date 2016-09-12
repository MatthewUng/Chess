import Board

class Tree:
    def __init__(self, board, turn):
        " 'white' or 'black' "
        self.root = Node(board, turn)
        self.depth = 0
        self.deepest = set()


    def newRoot(self, node):
        self.root = node
        self.depth = 0

    def implementLevel(self, n):
        
        self.depth += 1

    def minimax(self):
        

    class Node:
        def __init__(self,board, turn):
            self.board = board
            self.turn = turn
            self.children = list()
            self.parent = None

        def setParent(self, parent):
            self.parent = parent
        
        def implementChildren(self):
            

        def setChild(self, child):
            self.children.append(child)
        
        def getBoard(self):
            return self.board

class Bot:
    value = {'P':1,
             'N':3,
             'B':3,
             'R':5,
             'Q':9}

    def analyzeMaterial(board):
        white = 0
        black = 0
        for x in range(8):
            for y in range(8):
                if board[x][y][1] == 'white'
                    white += value[board[x][y][0]]
                else
                    black += value[board[x][y][0]]
        return (white, black)

if __name__ == '__main__':
    b = Board.Board()
    t = Tree(b, b.turn)

