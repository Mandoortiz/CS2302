"""
Author: Armando Ortiz
Course: CS 2302 Data Structures
Assignment: Lab 7
Instructor: Olac Fuentes
T.A.: Anindita Nath, Maliheh Zargaran
Last Modification: May 1, 2019
Purpose: The purpose of this lab is to modify the maze building program with new features
 - Allow the user to pick the number of walls to remove, while warning them if there might be less paths
 - create a graph of the adjacency list of open cells in the maze
 - Perform Breadth-First Search,Depth-First Search with stacks, and Depth-First Search using recursion
 - Display the path of these search functions in the maze
"""
import matplotlib.pyplot as plt
import numpy as np
import random
import time
import queue

# Initialize Disjoint Set Forest with size of maze
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

#Builds maze using union by size
def mazeUBS(walls,D,m):
    i = 0
    path = []#Array to build adjacent list of paths through maze
    while i <= m: #While there is more than one set 
       w = random.randint(0,len(walls)-1)# picks a random wall in the set
       c1 = find(D,walls[w][0])# Finds root of set
       c2 = find(D,walls[w][1])# Finds root of set
       if i >= len(D)-1:
           union(D,c1,c2)
           path.append(walls.pop(w))
           i+=1
       elif c1!= c2:# If sets are different
           union_by_size(D,c1,c2)# Uses union by compression
           path.append(walls.pop(w))#pops the wall while adding it to path array
           i +=1
    return path


def adjlist(L,n):
    AL = [[] for i in range(n)]
    for d in range(n):
        for j in range(len(L)):
            if L[j][0] <= d:
                if d == L[j][0]:
                    AL[d].append(L[j][1])
                elif d == L[j][1]:
                    AL[d].append(L[j][0])
    return AL

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

#Draws graph of connected vertices
def draw_graph(G,maze_rows,maze_cols):
    fig, ax = plt.subplots()
    for i in range(len(G)):
        for j in range(len(G[i])):
            if G[i][j] - i == 1:#horizontal lines
                x0 = i%maze_cols
                x1 = x0+1
                y0 = i//maze_cols
                y1 = y0
            elif G[i][j] - i == maze_cols:#vertical lines
                x0 = i%maze_cols
                x1 = x0
                y0 = i//maze_cols
                y1 = y0+1
            ax.plot([x0,x1],[y0,y1],linewidth=1,color='k')
    for r in range(maze_rows):
        for c in range(maze_cols):
            cell = c + r*maze_cols
            ax.text((c),(r),str(cell), size=8, ha="center", va="center",
                    bbox=dict(facecolor='w',boxstyle="circle"))
    
    ax.set_aspect(1.0)
    ax.axis('off') 

#Draws path through maze
def draw_path(walls,al,path,maze_rows,maze_cols):
    fig, ax = plt.subplots()
    for w in walls:#Draws walls of maze
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
    for i in range(len(path)-1):#Draws Path through maze
        if path[i+1] - path[i] == 1:#horizontal lines
            x0 = (path[i]%maze_cols)+.5#Centers path on the x-axis
            x1 = x0+1
            y0 = path[i]//maze_cols+.5
            y1 = y0
        elif path[i] - path[i+1] == 1:#horizontal lines
            x0 = (path[i]%maze_cols)+.5
            x1 = x0-1
            y0 = path[i]//maze_cols +.5
            y1 = y0
        elif path[i+1] - path[i] == maze_cols:#vertical lines
            x0 = (path[i]%maze_cols)+.5
            x1 = x0
            y0 = path[i]//maze_cols +.5
            y1 = y0+1
        elif path[i] - path[i+1] == maze_cols:#vertical lines
            x0 = (path[i]%maze_cols)+.5
            x1 = x0
            y0 = path[i]//maze_cols +.5
            y1 = y0-1
        ax.plot([x0,x1],[y0,y1],linewidth=1,color='r')
    
    fs = maze_rows*maze_cols-1
    if fs in al[path[-1]]:#if final item in path is points to 19
        if fs - path[-1] == 1:
            x0 = (path[-1]%maze_cols)+.5
            x1 = x0+1
            y0 = path[-1]//maze_cols+.5
            y1 = y0
        else:
            x0 = (path[-1]%maze_cols)+.5
            x1 = x0
            y0 = path[-1]//maze_cols +.5
            y1 = y0+1
        ax.plot([x0,x1],[y0,y1],linewidth=1,color='r')   
    ax.set_aspect(1.0)
    ax.axis('off') 

#Builds path through maze
def Path(prev,v,path):
    if prev[v] != -1:
        Path(prev,prev[v],path)
    path.append(v)

#Search Algorithms
# Breadth-first Search    
def breadthFirstSearch(G,v):
    visited = np.zeros(len(G),dtype = bool)
    prev = np.zeros(len(G),dtype=int)-1
    Q = queue.Queue(len(G))
    Q.put(v)
    visited[v] = True
    while Q.empty() == False:
        u = Q.get()
        for t in G[u]:
            if(visited[t]==False):
                visited[t] = True
                prev[t] = u
                Q.put(t)
    return prev

#Depth-first search using Stack
def depthFirstSearch(G,source):
    visited = np.zeros(len(G),dtype = bool)
    prev = np.zeros(len(G),dtype = int)-1
    stack = []
    stack.append(source)
    while len(stack) > 0:
        current = stack.pop()
        if visited[current] == False:
            visited[current] = True
            for i in G[current]:
                if visited[i] == False:
                    stack.append(i)
                    prev[i] = current
    return prev

#Depth-first search using recursion
def dfsrecursive(G,source,visited,prev):
    visited[source] = True
    for t in G[source]:
        if (visited[t] == False):
            prev[t] = source
            dfsrecursive(G,t,visited,prev)

plt.close("all") 
maze_rows = 15
maze_cols = 10
path = []
n = maze_rows*maze_cols
print("Number of Cells:",(n))

# Maze using regular union
walls = wall_list(maze_rows,maze_cols)
try:
    m = int(input("How many walls do you want to remove? "))
except:
    print("Invalid entry")
else:
    if m < n-1:
        print("A path is not guaranteed to exist.")
    elif m == n-1:
        print("There is a unique path to the destination")
    else:
        print("There is at least one from the source to destination")
    
    D = DisjointSetForest(maze_rows*maze_cols)
    
    try:
        path = mazeUBS(walls,D,m)
    except:
        print("Too many walls removed")
    else:
        al = adjlist(path,n)
        draw_graph(al,maze_rows,maze_cols)
        draw_maze(walls,maze_rows,maze_cols)
        
        # Breadth-First Search
        start = time.time()
        r = breadthFirstSearch(al,0)
        pathBFS = []
        Path(r,r[-1],pathBFS)
        draw_path(walls,al,pathBFS,maze_rows,maze_cols)
        end = time.time()
        rtBFS = end - start
        
        # Depth-First Search using Stack
        start = time.time()
        dfs = depthFirstSearch(al,0)
        pathDFS = []
        Path(dfs,dfs[-1],pathDFS)
        draw_path(walls,al,pathDFS,maze_rows,maze_cols)
        end = time.time()
        rtDFS = end-start
        
        # Depth-First Search using Recursion
        start = time.time()
        visit = np.zeros(len(al),dtype = bool)
        prev = np.zeros(len(al),dtype = int)-1
        dfsrecursive(al,0,visit,prev)
        pathDFSR =[]
        Path(prev,prev[-1],pathDFSR)
        draw_path(walls,al,pathDFSR,maze_rows,maze_cols)
        end = time.time()
        rtDFSR = end - start
        
        print("Breadth First Search runtime:",rtBFS)
        print("Depth First Search using Stack runtime:",rtDFS)
        print("Depth First Search using Recursion runtime:",rtDFSR)