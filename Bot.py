from collections import deque
import Board
import sys
import time

class Node:
    def __init__(self,board, move = None):
        self.board = board
        self.turn = self.board.turn
        self.children = list()
        self.parent = None
        #(board object, evaluation)
        self.evaluation = [None, None]
        self.alphabeta = [None,None]
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
        for child in self.children:
            child.parent = self

    def reset(self):
        self.evaluation = [None,None]
        self.alphabeta = [-9999999,9999999]
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
        self.minimax()
        return self.getEval()

    def minimax(self):
        #function determines the value of self node
        #while iterating through the tree
        if self.parent:
            self.alphabeta[0] = self.parent.alphabeta[0]
            self.alphabeta[1] = self.parent.alphabeta[1]


        #eval = (Node, eval)
        if self.isLeaf():
            self.setEval([self.moves, evaluate(self.board)])
            return
            

        for child in self.children:
            #obtain value of child
            child.minimax()

            #no choice made yet
            if not self.getEval()[1]:
                if self.turn == 'white':
                    self.setEval([child.moves, child.getEval()[1]])
                    if child.getEval()[1] > self.alphabeta[0]:
                        self.alphabeta[0] = child.getEval()[1]

                elif self.turn == 'black':
                    self.setEval([child.moves, child.getEval()[1]])
                    if child.getEval()[1] < self.alphabeta[1]:
                        self.alphabeta[1] = child.getEval()[1]

            #maximizer 
            if self.turn == 'white':
                #pruning
                if child.getEval()[1] > self.alphabeta[1]:
                    break
                elif child.getEval()[1] > self.getEval()[1]:
                    self.alphabeta[0] = child.getEval()[1]
                    self.setEval([child.moves, child.getEval()[1]])

            #minimizer
            elif self.turn == 'black':
                #pruning
                if child.getEval()[1] < self.alphabeta[0]:
                    break
                elif child.getEval()[1]< self.getEval()[1]:
                    self.alphabeta[1] = child.getEval()[1]
                    self.setEval([child.moves, child.getEval()[1]])

    def __repr__(self):
        return "<node: "+str(self.moves)+'eval: '+str(self.getEval())+\
        'a/b: '+str(self.alphabeta)+">"

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
        start = time.time()
        while n > self.depth:
            self.implementLevel()
            print 'current depth:', self.depth

        end = time.time()
        print '# leaf nodes: ', len(self.deepest), '\n'
        print "Took {} seconds to init tree".format(end - start)
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
    if mate[0]:
        out = -1000 if mate[1] == 'white' else 1000
        return out
    return mat + Range

def analyzeMate(board):
    if board.mateCheck('white'):
        return (True, 'white')
    elif board.mateCheck('black'):
        return (True,'black')
    return (False,'temp')

def analyzeRange(board):
    return len(board.attackRange(board.turn))* .02

def analyzeMaterial(board):
    board=board.getB()
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

