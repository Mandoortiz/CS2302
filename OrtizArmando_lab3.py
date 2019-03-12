"""
Author: Armando Ortiz
Course: CS 2302 Data Structures
Assignment: Lab 3
Instructor: Olac Fuentes
T.A.: Anindita Nath, Maliheh Zargaran
Last Modification: March 11, 2019
Purpose: The purpose of this program is to perform different operations using a Binary Search Tree
    -Display a drawing of a BST
    -Iteratively search for a key in a BST
    -Build a balanced tree using a sorted list.
    -Extracting the elements of a tree to create a sorted list
    -Print the keys of the tree by depth
"""
import numpy as np
import matplotlib.pyplot as plt
import math
import time

class BST(object):
    # Constructor
    def __init__(self, item, left=None, right=None):  
        self.item = item
        self.left = left 
        self.right = right      

#Meant to insert new node to tree        
def Insert(T,newItem):
    if T == None:
        T =  BST(newItem)
    elif T.item > newItem:
        T.left = Insert(T.left,newItem)
    else:
        T.right = Insert(T.right,newItem)
    return T

#Finds height of tree
def height(T):
    if T is None:
        return 0
    else:
        left = height(T.left)
        right = height(T.right)
    if left > right:
        return left + 1
    else:
        return right+1
         
def InOrderD(T,space):
    # Prints items and structure of BST
    if T is not None:
        InOrderD(T.right,space+'   ')
        print(space,T.item)
        InOrderD(T.left,space+'   ')

#Recursive Functions to find key in BST
def Find(T,k):
    # Returns the address of k in BST, or None if k is not in the tree
    if T is None or T.item == k:
        return T
    if T.item<k:
        return Find(T.right,k)
    return Find(T.left,k)

#Prints whether k is found or not
def FindAndPrint(T,k):
    f = Find(T,k)
    if f is not None:
        print(f.item,'found')
    else:
        print(k,'not found')

#Iterative Function to find key in BST    
def FindL(T,k):
    if T is None:
        return None
    while T.item is not None:
        if T.item == k:
            return T
        if T.item > k:
            if T.left is None:
                break
            T = T.left
        if T.item < k:
            if T.right is None:
                break
            T = T.right
    return None

#Prints whether key is found or not
def FindLAndPrint(T,k):
    f = FindL(T,k)
    if f is not None:
        print(f.item,'found')
    else:
        print(k,'not found')

#Creates a balanced tree using sorted List
def BalancedTree(L):
    if len(L)==0:
        return None
    mid = len(L)//2
    T = BST(L[mid])
    T.left = BalancedTree(L[:mid])
    T.right = BalancedTree(L[mid+1:])
    return T

#Builds a sorted list using BST
def BuildList(T,L):
    if T is not None:
        BuildList(T.left,L)
        L.append(T.item)
        BuildList(T.right,L)

#Function to print the keys of BST by Depth
def PrintAtDepth(T,d):
    i = 0
    z = height(T)
    while i < z :
      print("Keys at Depth", i ,end=': ')
      PrintDepth(T,0,i)
      print("")
      i +=1

#Function to move through tree to find       
def PrintDepth(T,d,k):
    if T is not None:
        if d == k:
            print(T.item,end=' ')
        PrintDepth(T.left,d+1,k)
        PrintDepth(T.right,d+1,k)

#Function for creating circle
def circle(cen,rad):
    n = int(4*rad*math.pi)
    t = np.linspace(0,6.3,n)
    x = cen[0]+rad*np.sin(t)
    y = cen[1]+rad*np.cos(t)
    return x,y

#Function to draw tree
def DrawTree(ax,T,line,x,y,r):
    if T is not None:
        left = [line[0]-x-(x+r),line[1]-y-r]#Creates new point for left branch
        right = [line[0]+x+(x+r),line[1]-y-r]#Creates new point for right branch
        x1,y1 = circle(line,r)#Outline circle
        r2 = r*.9#radius of inner circle
        x2,y2 = circle(line,r2)#Creates inner circle 
        if T.left is not None:
            ax.plot([line[0],left[0]],[line[1],left[1]],color = 'k',zorder=0)#Draws left branch
        if T.right is not None:
            ax.plot([line[0],right[0]],[line[1],right[1]],color='k',zorder=0)#Draws right branch
        ax.fill(x1, y1, 'k',x2,y2,'w',zorder=2)#Draws Circles
        ax.text(line[0]-r2*.5,line[1]-r2*.5,T.item,fontsize=10,zorder=3)#Places text inside of circle
        DrawTree(ax,T.left,left,x/2,y,r)
        DrawTree(ax,T.right,right,x/2,y,r)

T = None
A = [10,4,2,8,1,3,5,7,9,15,12,18]
for i in A:
    T = Insert(T,i)    
print("T")
InOrderD(T, ' ')

start = time.time()
PrintAtDepth(T,0)#Print keys by Depth
end = time.time()
print("Print Depths runtime: ",(end-start))
print("")

#Find recursively and iteratively
start = time.time()
FindLAndPrint(T,8)
end = time.time()
print("Search runtime: ",(end-start))

start = time.time()
FindLAndPrint(T,23)
end = time.time()
print("Search runtime: ",(end-start))

#Balanced Tree from Sorted List
print("")
print("T2")
B = [1,2,3,4,5,7,8,9,10,12,15,18]
start = time.time()
T2 = BalancedTree(B)
end = time.time()
print("Building Tree runtime: ",(end-start))

print(" ")
InOrderD(T2, ' ')
start = time.time()
PrintAtDepth(T2,0)
end = time.time()
print("Print Depths runtime: ",(end-start))

#Build List using Tree
L = []
start = time.time()
BuildList(T,L)
end = time.time()
print("Sorted List runtime: ",(end-start))
print(L)

#Drawing the binary search tree
plt.close("all")
fig, ax = plt.subplots()
line = np.array([0,0])
start = time.time()
DrawTree(ax,T,line,100,100,40)
end = time.time()
print("Drawing Tree runtime: ",(end-start))
ax.set_aspect(1.0)
ax.axis('off')
plt.show()
fig.savefig('BTree.png')
