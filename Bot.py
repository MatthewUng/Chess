from collections import deque
import Board
import time

class Node:
    def __init__(self,board, move = None):
        self.board = board
        self.turn = self.board.turn
        self.children = list()
        self.parent = None
        self.evaluation = None #(board object, evaluation)
        if move == None:
            self.moves = list()
        else:
            self.moves = move

    def parseLevel(self):
        posneg = 1 if self.turn == 'white' else -1
        self.evaluation = max(self.children, key = posneg * evaluate)
        return self.evaluation

    def implementChildren(self):
        """implement all the possible children for the node"""
        for move in self.board.getMoves(self.turn):
            temp = self.moves[:]
            temp.append(move)
            self.setChild(Node(self.board.implementMove(move), temp))
            
    def reset(self):
        self.evaluation = None
        #propagate down
        for node in self.children:
            node.reset()

    def isLeaf(self):
        if not self.children:
            return True
        else: return False

    def setEval(self, value):
        self.evaluation = value

    def getEval(self):
        return self.evaluation

    def setChild(self, child):
        self.children.append(child)

    def setParent(self, parent):
        self.parent = parent

    def getChildren(self):
        return self.children
    
    def getParent(self):
        return self.parent

    def getBoard(self):
        return self.board
    
    def hasChildren(self):
        return bool(self.children)

    def findBest(self):
        """self node is the root node"""
        self.minimax(None, None)
        return self.getEval()

    def minimax(self, alpha, beta):
        #function determines the value of self node
        #while iterating through the tree
        if self.isLeaf():
            self.setEval((None, evaluate(self.getBoard())))
            return

        for child in self.children:
            #obtain value of child
            child.minimax(alpha,beta) 
            #no choice made yet
            if not self.getEval():
                self.setEval(child.getEval())

            #maximizer 
            if self.turn == 'white':
                #pruning
                if child.getEval() < beta:
#                    self.setEval((child, child.getEval()))
                    break
                elif child.getEval()[1] > self.getEval()[1]:
                    self.setEval((child, child.getEval()[1])) 
                    alpha = child.getEval()

            #minimizer
            elif self.turn == 'black':
                #pruning
                if child.getEval()[1] > alpha:
#                    self.setEval((child, child.getEval()[1]))
                    break
                elif child.getEval()[1]< self.getEval()[1]:
                    self.setEval((child, child.getEval()[1])) 
                    beta = child.getEval()

    def __repr__(self):
        return "node: "+str(self.moves)

class Tree:

    def __init__(self, board, turn):
        " 'white' or 'black' "
        self.root = Node(board)
        self.depth = 0
        self.deepest = set([self.root]) #set of nodes in the last level
        

    def newRoot(self, node):
        self.root = node
        self.depth = 0

    def getLevel(self, node, level):
        if level == 0:
            return list(node)
        out = list()
        for child in self.root.getChildren:
            out.extend(self.getLevel(child, level-1))
        return out

    def getLastLevel(self):
        pass
    
    def reset(self):
        self.root.reset()

    def implementLevel(self):
        newDeep = set()
        for node in self.deepest:
            node.implementChildren()
            newDeep |= set(node.getChildren())
        self.deepest = newDeep
        self.depth += 1
        
    def minimax(self, n):
        while n > self.depth:
            self.implementLevel()
            print 'ok'
        print len(self.deepest)
        self.reset()
        out = self.root.findBest()
        return out

    def __repr__(self):
        out = ''
        queue = deque()
        queue.append(self.root)
        nextRow = list()

        while queue:
            Next = queue.popleft()   
            out += str(Next)
            if Next == '\n':
                queue.append(nextRow)
                nextRow.clear()

            elif type(Next) == list:
                out += ''

            elif Next.hasChildren():
                nextRow.append(Next.getChildren())

            if not queue and nextRow:
                queue.append('\n')
        return out

    def test(self):
        print '\n\nzeroth: \n\n'+str(self.deepest)
        self.implementLevel()
        print '\n\nfirst: \n\n' +str(self.deepest)
        self.implementLevel()
        print '\n\nsecond: \n\n'+str(self.deepest)
        exit()

class Bot:
    value = {'P':1,
             'N':3,
             'B':3,
             'R':5,
             'Q':9}

value = {'P':1,
         'N':3,
         'B':3,
         'R':5,
         'Q':9,
         'K':0}

def evaluate(board):
    """board is board object"""
    mat = analyzeMaterial(board)
    mate = analyzeMate(board)
    Range = analyzeRange(board)
    return mat + mate + Range

def analyzeMate(board):
    if board.mateCheck('white'):
        return -1000.0
    elif board.mateCheck('black'):
        return 1000.0
    return 0.0

def analyzeRange(board):
    return len(board.attackRange(board.turn))* .02

def analyzeMaterial(board):
    board=board.getD()
    white = 0
    black = 0
    for x in range(8):
        for y in range(8):
            if board[x][y][1] == 'white':
                white += value[board[x][y][0]]
            elif board[x][y][1] == 'black':
                black += value[board[x][y][0]]
    return float(white - black)

if __name__ == '__main__':
    f = open('matein2.txt','r')
    fen = f.read()
    b = Board.Board()
    b.setUp(fen)
    print b

    t = Tree(b, b.turn) 
    start_time = time.time()
    print t.minimax(3)
    end_time = time.time()
    print "{} seconds to compute".format(end_time - start_time)

