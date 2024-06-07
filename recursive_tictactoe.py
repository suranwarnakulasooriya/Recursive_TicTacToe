# DEPENDENCIES ====================================================================================

import pygame, argparse # i/o and argument parsing
from random import randint,choice # to create ranodm moves during autoplay

# PARSE ===========================================================================================

parser = argparse.ArgumentParser(prog='Recursive TicTacToe',
    description='A pygame-based program that runs tic tac toe recursively at an arbitrary depth.')

parser.add_argument('-d','--depth',type=int,default=1,help='game depth (at least 1)') # depth
parser.add_argument('-a','--autoplay',type=bool,action=argparse.BooleanOptionalAction, # autoplay
                    help='have the game play itself')
parser.add_argument('-s','--size',type=int,default=800,help='screen size in pizels') # size

# BACKEND INIT ====================================================================================

args = parser.parse_args() # get args
depth = max(1,args.depth) # number of levels of recursion (1 = normal game)
autoplay = args.autoplay # if the game plays itself
target_sidelength = max(100,args.size) # target sidelength of screen in pixels

# closest integer to target_sidelength divisible by 3^depth so every cell has an integer sidelength
sl = (target_sidelength//(3**depth))*(3**depth) 

winlines = ((0, 1, 2),(3, 4, 5),(6, 7, 8),(0, 3, 6), # if these sets of indices match,
            (1, 4, 7),(2, 5, 8),(0, 4, 8),(2, 4, 6)) # there is a winner

symboldict = {-1:'O', 1:'X', 0:'·'} # -1 is O, 1 is X, O is empty/unsolved
unsolved_boards = [] # list of paths of unsolved boards
gameover = 0
turn = 1 # X starts first
path = [] # inititial path that the move has to match ([] means any path)

# BOARD CLASS =====================================================================================

class board:
    def __init__(self,depth,path=[],parent=None):
        self.is_deepest = not depth-1 # if this board has a depth of 1 (no child boards)
        self.is_solved = False; self.state = 0 # starts unsolved (0)
        self.substates = [0]*9 # states of children
        self.path = path # list of indices within parent boards to get to this board

        if not self.is_deepest: # create child boards, add indices to each child's path
            self.children = [board(depth-1,self.path+[0],self),
                             board(depth-1,self.path+[1],self),
                             board(depth-1,self.path+[2],self),
                             board(depth-1,self.path+[3],self),
                             board(depth-1,self.path+[4],self),
                             board(depth-1,self.path+[5],self),
                             board(depth-1,self.path+[6],self),
                             board(depth-1,self.path+[7],self),
                             board(depth-1,self.path+[8],self)]
        else: self.children = self.substates # if this board is the deepest, its children are cells

        unsolved_boards.append(self.path) # add path to unsolved_boards

    def update_state(self):
        if not self.is_deepest: self.substates = [child.update_state() for child in self.children]
        self.state = checkwin(self.substates,winlines) # check if this board is solved
        if self.state: self.solve() # declare self and children as solved if state != 0
        return self.state
        
    def solve(self): # declare self and all children as soled and remove from unsolved boards
        self.is_solved = True
        try: unsolved_boards.remove(self.path) # remove path from unsolved_boards
        except: pass
        if not self.is_deepest: # solve children
            for child in self.children: child.solve()

    def reset(self): # reset self and children
        self.is_solved = False
        self.state = 0
        self.substates = [0]*9
        unsolved_boards.append(self.path)
        if not self.is_deepest:
            for child in self.children: child.reset()
        else:
            self.children = self.substates

# BACKEND METHODS =================================================================================

def checkwin(board,lines=winlines): # return the winner of a single (depth 1) board
    for line in lines: # check each winline
        if board[line[0]] == board[line[1]] == board[line[2]] != 0:
            return board[line[0]] # return the winner (-1 or 1) of there is one
    if 0 not in board: return 2 # return 2 (tie) if no open spaces left
    return 0 # otherwise return 0 (unsolved)

def get_cell(r,c,S,depth,board,path,e=0): # given screen coords: get target board, index, and path
    y,x = r*3//S,c*3//S # get board coords from screen coords
    dy,dx = r-y*S//3,c-x*S//3 # screen coords of topleft of current cell/board (offset)
    e = 3*y+x # index of cell/board at current depth
    path.append(e) # add index to path
    if board.is_deepest: return e,board,path
    return get_cell(dy,dx,S//3,depth-1,board.children[e],path,e)

def update_path(path): # if the intended path is solved, go one level up
    if path not in unsolved_boards: return path[:-1]
    return path

# FRONTEND METHODS ================================================================================

def draw_blank(p,y=0,x=0,w=depth,dy=0,dx=0):
    return # this function is index 0 in `shapes`, meaning blank, so it does nothing

def draw_X(p,y=0,x=0,w=depth,dy=0,dx=0): # draw X with given coords, cell size, and thickness
    pygame.draw.line(screen,Xcolor,(dx+p*x,dy+p*y),(dx+p*(x+1),dy+p*(y+1)),width=w)
    pygame.draw.line(screen,Xcolor,(dx+p*(x+1),dy+p*y),(dx+p*x,dy+p*(y+1)),width=w)

def draw_O(p,y=0,x=0,w=depth,dy=0,dx=0): # draw O with given coords, cell size, and thickness
    pygame.draw.circle(screen,Ocolor,(dx+p*(x+0.5),dy+p*(y+0.5)),p//2,width=w)

def draw_tie(p,y=0,x=0,w=2,dy=0,dx=0): # draw tie (+) with given coords, cell size, and thickness
    pygame.draw.line(screen,Tcolor,(dx+x*p,dy+(y+.5)*p),(dx+x*p+p,dy+(y+.5)*p),width=w)
    pygame.draw.line(screen,Tcolor,(dx+(x+.5)*p,dy+y*p),(dx+(x+.5)*p,dy+y*p+p),width=w)

def draw_lines(x=0,y=0,S=sl,depth=depth): # draw lines given screen size, depth, and offsets
    if depth == 0: return # can't draw depth 0
    p = S//3

    for i in range(1,3): # draw two horizonal and vertical lines
        pygame.draw.line(screen,Lcolor,(x,i*p+y),(S+x,i*p+y),width=depth)
        pygame.draw.line(screen,Lcolor,(i*p+x,y),(i*p+x,S+y),width=depth)

    for i in range(3): # draw 9 child sets of lines
        for j in range(3): draw_lines(x+i*p,y+j*p,p,depth-1)

def draw_board(board,x=0,y=0,S=sl,depth=depth):
    p = S//3
    if board.is_deepest: # if this is a deep board
        for i,cell in enumerate(board.substates): # draw cells with offset based on index & offsets
            shapes[cell](p,i//3,i%3,depth,y,x)
        shapes[board.state](S,0,0,depth+1,y,x) # draw overall board state (nothing if unsolved)
        return # break

    for e in range(9): # draw child boards if this isn't the deepest board
        draw_board(board.children[e],x+e%3*p,y+e//3*p,p,depth-1)

    shapes[board.state](S,0,0,depth+1,y,x) # draw overall board state
    
def draw_square(path,S=sl,depth=depth): # draw a square to highlight the active region
    if path != []:
        x,y = 0,0; p = S # offsets start as 0, cell size starts as screensize
        for i in path: # iterate through each index in path
            p //= 3 # cell size thirds with each recursion
            y += p*(i//3); x += p*(i%3) # add offsets based on index
        pygame.draw.rect(screen,Hcolor,((x,y),(p,p)))

def render(): # render lines and board, then refresh
    screen.fill(Bcolor)
    if depth > 1 and not gameover: draw_square(path)
    draw_lines(); draw_board(mainboard); pygame.display.update()

# FRONTEND INIT ===================================================================================

if __name__ == '__main__':
    shapes = (draw_blank,draw_X,draw_tie,draw_O) # tup of draw functions

    Bcolor = 0x141414 # background
    Hcolor = Bcolor*2 # active region highlight
    Lcolor = Bcolor*3 # lines
    Tcolor = Bcolor*4 # tie
    Xcolor = 0xcc6666
    Ocolor = 0x81a2be

    mainboard = board(depth)

    pygame.init(); screen = pygame.display.set_mode((sl,sl)); render()

# MAINLOOP ========================================================================================

while __name__ == '__main__':
    for event in pygame.event.get(): # exit conditions
        if event.type == pygame.QUIT: exit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE] or keys[pygame.K_q]: exit()

    valid_change = 0 # only update when there is a valid change instead of every frame
    pygame.display.set_caption(f"Recursive TicTacToe | Depth {depth} | {symboldict[turn] \
                                 if not gameover else 'R to restart'}")

    # on click/auto
    if not gameover and ((autoplay) or (not autoplay and pygame.mouse.get_pressed()[0])):
        if not autoplay: pos = pygame.mouse.get_pos() # get mouse position on click
        else:
            randompath = path[:] # generate random path on autopley

            if len(unsolved_boards) > 10 or path != []: # random list of indices
                while len(randompath) < depth: randompath.append(randint(0,8))
            else: # or pick one of the few remaining available paths and pick one more random index
                randompath = choice(unsolved_boards)[:]; randompath.append(randint(0,8))
                
            p = sl # create screen coords based on randomly generated path
            y,x = 0,0 # offsets start as 0
            for i in randompath: p //= 3; y += p*(i//3); x += p*(i%3)
            pos = (x,y)

        # get index, board, and path from screen coords
        e,target_board,trypath = get_cell(pos[1],pos[0],sl,depth,mainboard,[])

        test_trypath = trypath[:]
        while len(test_trypath) > len(path): test_trypath.pop(-1) # make paths the same length

        if (not target_board.children[e] and not target_board.is_solved) and \
           ((path == []) or (path == test_trypath != [])):
            valid_change = 1 # a valid click happened so the game must re-render
            target_board.children[e] = turn # change cell
            turn *= -1 # change turn
            mainboard.update_state() # update game state
            path = trypath # set new path

    while len(path) > depth-1: path.pop(0) # make path matches depth
    path = update_path(path) # reduce path if needed

    if mainboard.is_solved: gameover = 1 # declare gameover if the mainboard is solved

    if gameover and keys[pygame.K_r]: # reset on r
        unsolved_boards = []; mainboard.reset() # reset all boards and refill unsolved_boards
        gameover = 0; turn = 1; valid_change = 0; render() # new game starts with X

    if valid_change: render() # render if the game state has changed
