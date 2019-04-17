"""
Author: Armando Ortiz
Course: CS 2302 Data Structures
Assignment: Lab 6
Instructor: Olac Fuentes
T.A.: Anindita Nath, Maliheh Zargaran
Last Modification: April 16, 2019
Purpose: The purpose of this program is to create two mazes
    - one using union
    - one using union by size which uses path compression
"""
import matplotlib.pyplot as plt
import numpy as np
import random
import time

def DisjointSetForest(size):
    return np.zeros(size,dtype=np.int)-1
        
def find(S,i):
    # Returns root of tree that i belongs to
    if S[i]<0:
        return i
    return find(S,S[i])

def find_c(S,i): #Find with path compression 
    if S[i]<0: 
        return i
    r = find_c(S,S[i]) 
    S[i] = r 
    return r
    
def union(S,i,j):
    # Joins i's tree and j's tree, if they are different
    ri = find(S,i) 
    rj = find(S,j)
    if ri!=rj:
        S[rj] = ri

def union_c(S,i,j):
    # Joins i's tree and j's tree, if they are different
    # Uses path compression
    ri = find_c(S,i) 
    rj = find_c(S,j)
    if ri!=rj:
        S[rj] = ri
         
def union_by_size(S,i,j):
    # if i is a root, S[i] = -number of elements in tree (set)
    # Makes root of smaller tree point to root of larger tree 
    # Uses path compression
    ri = find_c(S,i) 
    rj = find_c(S,j)
    if ri!=rj:
        if S[ri]>S[rj]: # j's tree is larger
            S[rj] += S[ri]
            S[ri] = rj
        else:
            S[ri] += S[rj]
            S[rj] = ri

# Draws the maze
def draw_maze(walls,maze_rows,maze_cols,cell_nums=False):
    fig, ax = plt.subplots()
    for w in walls:
        if w[1]-w[0] ==1: #vertical wall
            x0 = (w[1]%maze_cols)
            x1 = x0
            y0 = (w[1]//maze_cols)
            y1 = y0+1
        else:#horizontal wall
            x0 = (w[0]%maze_cols)
            x1 = x0+1
            y0 = (w[1]//maze_cols)
            y1 = y0  
        ax.plot([x0,x1],[y0,y1],linewidth=1,color='k')
    sx = maze_cols
    sy = maze_rows
    ax.plot([0,0,sx,sx,0],[0,sy,sy,0,0],linewidth=2,color='k')
    if cell_nums:
        for r in range(maze_rows):
            for c in range(maze_cols):
                cell = c + r*maze_cols   
                ax.text((c+.5),(r+.5), str(cell), size=10,
                        ha="center", va="center")
    ax.axis('off') 
    ax.set_aspect(1.0)

def wall_list(maze_rows, maze_cols):
    # Creates a list with all the walls in the maze
    w =[]
    for r in range(maze_rows):
        for c in range(maze_cols):
            cell = c + r*maze_cols
            if c!=maze_cols-1:
                w.append([cell,cell+1])
            if r!=maze_rows-1:
                w.append([cell,cell+maze_cols])
    return w

# Create Maze using Union
def mazeU(walls,D):
    sets = len(D)
    while sets>1:# While there is more than one set
        w = random.randint(0,len(walls)-1)# picks a random wall in the set
        c1 = find(D,walls[w][0])# Finds root of set
        c2 = find(D,walls[w][1])# Finds root of Set
        if c1 != c2:# If sets are different
            union(D,c1,c2)# uses Union
            sets-=1
            walls.pop(w)# removes wall

# Create Maze using Union By Size
def mazeUBS(walls,D):
    sets = len(D)
    while sets >1: #While there is more than one set 
       w = random.randint(0,len(walls)-1)#npicks a random wall in the set
       c1 = find(D,walls[w][0])#nFinds root of set
       c2 = find(D,walls[w][1])#nFinds root of set
       if c1!= c2:#nIf sets are different
           union_by_size(D,c1,c2)# Uses union by compression
           sets -=1
           walls.pop(w)# removes wall
plt.close("all") 

maze_rows = 10
maze_cols = 15

# Maze using regular union
walls = wall_list(maze_rows,maze_cols)
D1 = DisjointSetForest(maze_rows*maze_cols)
start = time.time()
mazeU(walls,D1)
end = time.time()
mazeURuntime = end - start
print("Maze by union runtime",mazeURuntime)
draw_maze(walls,maze_rows,maze_cols)

# Maze using union by size
walls2 = wall_list(maze_rows,maze_cols)
D2 = DisjointSetForest(maze_rows*maze_cols)
start = time.time()
mazeUBS(walls2,D2)
end = time.time()
mazeUBSRuntime = end - start
print("Maze by union by size runtime",mazeUBSRuntime)
draw_maze(walls2,maze_rows,maze_cols) 