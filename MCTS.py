import math
from path_search import *
from sys import float_info
"""
Monte carlo theory implementation
"""
class GameState:
    def __init__(self):
        self.tiles=None
        self.paths=[]
        self.pacman=None
        self.ghosts=[]
        self.isLeaf=True
        self.children=[]
        self.score=0
        self.n=1#number of times simulated
        self.v=0#is used for selection
        self.M=0#maximum mean reward
    
"""
selects a node
"""
def select(node,height,path):
    if node.isLeaf:
        node.M=expand(node)
        node.n+=1
        for i in range(len(path)-1,-1,-1):
            path[i].n+=1
            path[i].M=max(temp.M for temp in path[i].children)
    else:
        """
        selecting the node which has the best UCT(upper confidence bound)
        """
        path.append(node)
        X=(-1000000000,node.children[0])
        for child in node.children:
            val=UCT(child.v,node.n,child.n)
            if(child.score==160):
                return
            if X[0]<val and (child.n/node.n)<0.9:
                X=(val,child)
        select(X[1],height+1,path)

def UCT(v,total,current):
    return v+100*math.sqrt(math.log(total)/(current))

def expand(node):
    '''
    expands the node and returns the maximum value of the expanded children
    '''
    p=node.pacman
    max1=-100000
    for tup in {(0,-1),(-1,0),(0,1),(1,0)}:
        inValid_move=False
        if node.tiles[p[0]+tup[0]][p[1]+tup[1]]!=0:
            child= GameState()
            child.tiles=b = [x[:] for x in node.tiles]
            child.score=node.score
            child.pacman=(p[0]+tup[0],p[1]+tup[1])
            if node.tiles[p[0]+tup[0]][p[1]+tup[1]]==1:
                child.score+=1
                child.tiles[p[0]+tup[0]][p[1]+tup[1]]=2

            for i in range(len(node.ghosts)):
                t1=node.ghosts[i]
                t2=node.paths[i][0]
                ghost=(t1[0]+t2[0],t1[1]+t2[1])

                if t1==child.pacman or ghost==child.pacman:
                    inValid_move=True
                    break
                ghost_path=[]
                if (i==0 or i==4) and len(node.paths[i])>2 :#ith ghost will chase the future pacman move
                    if node.tiles[ghost[0]][ghost[1]]==0:
                        ghost=tuple(node.ghosts[i])
                    pat=(child.pacman[0]+tup[0],child.pacman[1]+tup[1])
                    pat2=(child.pacman[0]+2*tup[0],child.pacman[1]+2*tup[1])
                    if(child.tiles[pat2[0]][pat2[1]]!=0) and len(node.paths[i])>3:
                        ghost_path=findPacman(child.tiles,pat2,ghost)
                    else:
                        ghost_path=findPacman(child.tiles,pat,ghost)
                else:#will chase the pacman
                    ghost_path=findPacman(child.tiles,child.pacman,ghost)
                if(len(ghost_path)==0):
                        ghost_path=[(0,0)]
                child.paths.append(ghost_path)
                child.ghosts.append(ghost)
            if inValid_move:
                continue
            child.v=child.M=ghostFactor(child.paths)+scoreFactor(child.score)
            max1=max(max1,child.M)
            node.children.append(child)
    if len(node.children)!=0:
        node.tiles=None
        node.ghosts=None
        node.isLeaf=False       
    return max1

def ghostFactor(paths):
    s=0
    for path in paths:
        x=len(path)
        epsilon=float_info.epsilon
        s+=300-300*(math.exp(-(x/4)))
    return s

def scoreFactor(score):
    return score*score
    #return 5*(score+math.exp(score/40))
            
            
    
    
    
    
