"""Pacman, classic arcade game.

Exercises

1. Change the board.
2. Change the number of ghosts.
3. Change where pacman starts.
4. Make the ghosts faster/slower.
5. Make the ghosts smarter.

"""
from path_search import *
from MCTS import *
from random import choice
from turtle import *
import time
from freegames import floor, vector
frame=1
state = {'score': 0}
path = Turtle(visible=False)
writer = Turtle(visible=False)
aim = vector(5, 0)
pacman = vector(-40, -80)
pac_man=Turtle(visible=True)
pac_man.penup()
ghosts = [
    [vector(-180, 160), vector(5, 0)],
    [vector(-180, -160), vector(0, 5)],
    [vector(100, 160), vector(0, -5)],
    #[vector(100, -160), vector(-5, 0)],
]
# fmt: off
tiles = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
# fmt: on
monte_carlo_tree =None

def square(x, y):
    "Draw square using path at (x, y)."
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()

    for count in range(4):
        path.forward(20)
        path.left(90)

    path.end_fill()


def offset(point):
    "Return offset of point in tiles."
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    #index = int(x + y * 20)
    return int(y),int(x)


def valid(point):
    "Return True if point is valid in tiles."
    r,c = offset(point)

    if tiles[r][c] == 0:
        return False

    r,c = offset(point + 19)

    if tiles[r][c] == 0:
        return False

    return point.x % 20 == 0 or point.y % 20 == 0


def world():
    "Draw world using path."
    bgcolor('blue')
    path.color('black')

    for r in range(len(tiles)):
        for c in range(len(tiles[0])):
            tile = tiles[r][c]

            if tile > 0:
                x = (c) * 20 - 200
                y = 180 - (r) * 20
                square(x, y)

                if tile == 1:
                    path.up()
                    path.goto(x + 10, y + 10)
                    path.dot(4, 'yellow')
    for arr in ghosts:
        turt=Turtle()
        turt.penup()
        arr.append(turt)
    



def move():
    "Move pacman and all ghosts."
    global monte_carlo_tree
    writer.undo()
    writer.write(state['score'])
    for i in range(200):
        select(monte_carlo_tree,0,[])
    for i in range(len(ghosts)):
        point, course,cursor=ghosts[i]
        global route;
        if frame%4 ==1:
            route[i]=monte_carlo_tree.paths[i]   
        vec =vector(5*route[i][0][1],(-5)*route[i][0][0])
        course.x=vec.x
        course.y=vec.y
        
        point.move(course)
      
        up()
        cursor.goto(point.x+10, point.y+10)
        if i==0:
            renderPinkyGhost(cursor)
        else:
            renderGhost(cursor)
    clear()
    if frame%4==1:
        best_state=(-10000,None)
        for child in monte_carlo_tree.children:
            if best_state[0]< child.M:
                best_state=(child.M,child)
        monte_carlo_tree=best_state[1]
        p=offset(pacman)
        b=best_state[1].pacman
        aim.x=5*(b[1]-p[1])
        aim.y=-5*(b[0]-p[0])  
    pacman.move(aim)

    r,c = offset(pacman)

    if tiles[r][c] == 1:
        tiles[r][c] = 2
        state['score'] += 1
        x = (c) * 20 - 200
        y = 180 - (r) * 20
        square(x, y)

    up()  
    pac_man.goto(pacman.x + 10, pacman.y + 10)
    renderPacman()
    goto(pacman.x + 10, pacman.y + 10)
    #dot(20, 'yellow')

    update()
    
    for point, course,cursor in ghosts:
        if abs(pacman - point) < 10:
            pass
            return False

    return True
     
def renderPacman():
    global frame
    pac_man.shape("circle")
    if frame%3==1:
        pac_man.shape("pacman1.gif")
    elif frame%3==2:
        pac_man.shape("pacman2.gif")
    else:
        pac_man.shape("pacman3.gif")
    frame+=1
    if(frame==12):
        frame=0
        
def renderGhost(ghost):
    ghost.shape("circle")
    if frame%2==1:
        ghost.shape("ghost1.gif")
    else:
        ghost.shape("ghost2.gif")
def renderPinkyGhost(ghost):
    ghost.shape("circle")
    if frame%2==1:
        ghost.shape("pinky1.gif")
    else:
        ghost.shape("pinky2.gif")
def registerAssets():
    screen=Screen()
    screen.register_shape('ghost1.gif')
    screen.register_shape('ghost2.gif')
    screen.register_shape('pinky1.gif')
    screen.register_shape('pinky2.gif')
    screen.register_shape('pacman1.gif')
    screen.register_shape('pacman2.gif')
    screen.register_shape('pacman3.gif')
route={}

monte_carlo_tree=GameState()
monte_carlo_tree.tiles=list(tiles)
monte_carlo_tree.pacman=offset(pacman)
monte_carlo_tree.ghosts=[]
monte_carlo_tree.paths=[]
for ghost in ghosts:
    monte_carlo_tree.ghosts.append(offset(ghost[0]))
    monte_carlo_tree.paths.append(findPacman(tiles,offset(pacman),offset(ghost[0])))
registerAssets()
setup(420, 420, 370, 0)
hideturtle()
tracer(False)
writer.goto(160, 160)
writer.color('white')
writer.write(state['score'])
world()
while move():
    pass
done()
