from queue import PriorityQueue
from pandas import *
import math
"""
    A* algorithm for ghosts for pathfinding
"""
def findPacman(tiles,pacman,ghost):
    
    mat = list(map(lambda x:list(map(lambda x:None,range(len(tiles[0])))),range(len(tiles))))
    mat[ghost[0]][ghost[1]]=ghost
    que=PriorityQueue();
    que.put((1,ghost))
    found=False
    while not (que.qsize()<=0 or found):
        """x = mat
        print (DataFrame(x).to_string())
        print("\n")"""
        r,c=que.get()[1]
        for (x,y) in [(0,-1),(-1,0),(0,1),(1,0)]:
            
            if tiles[r+x][c+y]!=0 and mat[r+x][c+y]==None:
                mat[r+x][c+y]=(r,c)
                if(r+x,c+y)==pacman:
                    found=True
                    break;
                #g=abs(ghost[0]-(r+x))+abs(ghost[1]-(c+y))
                g=math.sqrt((ghost[0]-(r+x))**2+(ghost[1]-(c+y))**2)
                #h=abs(pacman[0]-(r+x))+abs(pacman[1]-(c+y))
                h=math.sqrt((pacman[0]-(r+x))**2+(pacman[1]-(c+y))**2)
                que.put((g+h,(r+x,c+y)))
            elif(r+x,c+y)==pacman:
                mat[r+x][c+y]=(r,c)
                found=True
                break;
    if not found:
        return None
    path=[]
    tup=pacman
    while tup!=ghost:
        x,y=tup
        path.append((x,y))
        tup=mat[x][y]

    path.reverse()
    prev=ghost
    for i in range(len(path)):
        path[i],prev=(path[i][0]-prev[0],path[i][1]-prev[1]),path[i]
    #print(path)
    return path
        
        
