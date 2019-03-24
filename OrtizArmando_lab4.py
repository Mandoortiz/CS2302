"""
Author: Armando Ortiz
Course: CS 2302 Data Structures
Assignment: Lab 4
Instructor: Olac Fuentes
T.A.: Anindita Nath, Maliheh Zargaran
Last Modification: March 24, 2019
Purpose: The purpose of this program is to use a B-tree to create basic functions that:
    - Compute the height of the tree
    - Extract the items into a sorted list
    - Return the min and max elements in the tree
    - Return number of nodes at a certain depth, nodes that are full, and leaves that are full
    - Print the nodes at a certain depth
    - Find the depth of an item in the tree, or -1 if the item is not in the tree
"""
import math
import time
class BTree(object):
    # Constructor
    def __init__(self,item=[],child=[],isLeaf=True,max_items=5):  
        self.item = item
        self.child = child 
        self.isLeaf = isLeaf
        if max_items <3: #max_items must be odd and greater or equal to 3
            max_items = 3
        if max_items%2 == 0: #max_items must be odd and greater or equal to 3
            max_items +=1
        self.max_items = max_items

def FindChild(T,k):
    # Determines value of c, such that k must be in subtree T.child[c], if k is in the BTree    
    for i in range(len(T.item)):
        if k < T.item[i]:
            return i
    return len(T.item)
             
def InsertInternal(T,i):
    # T cannot be Full
    if T.isLeaf:
        InsertLeaf(T,i)
    else:
        k = FindChild(T,i)   
        if IsFull(T.child[k]):
            m, l, r = Split(T.child[k])
            T.item.insert(k,m) 
            T.child[k] = l
            T.child.insert(k+1,r) 
            k = FindChild(T,i)  
        InsertInternal(T.child[k],i)   
            
def Split(T):
    #print('Splitting')
    #PrintNode(T)
    mid = T.max_items//2
    if T.isLeaf:
        leftChild = BTree(T.item[:mid]) 
        rightChild = BTree(T.item[mid+1:]) 
    else:
        leftChild = BTree(T.item[:mid],T.child[:mid+1],T.isLeaf) 
        rightChild = BTree(T.item[mid+1:],T.child[mid+1:],T.isLeaf) 
    return T.item[mid], leftChild,  rightChild   
      
def InsertLeaf(T,i):
    T.item.append(i)  
    T.item.sort()

def IsFull(T):
    return len(T.item) >= T.max_items

def Insert(T,i):
    if not IsFull(T):
        InsertInternal(T,i)
    else:
        m, l, r = Split(T)
        T.item =[m]
        T.child = [l,r]
        T.isLeaf = False
        k = FindChild(T,i)  
        InsertInternal(T.child[k],i)   
               
def Search(T,k):
    # Returns node where k is, or None if k is not in the tree
    if k in T.item:
        return T
    if T.isLeaf:
        return None
    return Search(T.child[FindChild(T,k)],k)
                  
def Print(T):
    # Prints items in tree in ascending order
    if T.isLeaf:
        for t in T.item:
            print(t,end=' ')
    else:
        for i in range(len(T.item)):
            Print(T.child[i])
            print(T.item[i],end=' ')
        Print(T.child[len(T.item)])    
 
def PrintD(T,space):
    # Prints items and structure of B-tree
    if T.isLeaf:
        for i in range(len(T.item)-1,-1,-1):
            print(space,T.item[i])
    else:
        PrintD(T.child[len(T.item)],space+'   ')  
        for i in range(len(T.item)-1,-1,-1):
            print(space,T.item[i])
            PrintD(T.child[i],space+'   ')

# Returns height of tree
def height(T):
    if T.isLeaf:
        return 0
    return 1 + height(T.child[0])

# Creates sorted list using B-Tree
def SortedList(T,L):
    if T.isLeaf:
        for t in range(len(T.item)):
            L.append(T.item[t])
    else:
        for i in range(len(T.item)):
            SortedList(T.child[i],L)
            L.append(T.item[i])
        SortedList(T.child[len(T.item)],L)
 
# Finds smallest item at depth d
def MinAtDepth(T,d):
    if d == 0:
        print(T.item[0])
        return T.item[0]
    if T.isLeaf:
        return math.inf
    return MinAtDepth(T.child[0],d-1)

# Finds largest item at depth d    
def MaxAtDepth(T,d):
    if d == 0:
        print(T.item[-1])
        return T.item[-1]
    if T.isLeaf:
        return -math.inf
    return MaxAtDepth(T.child[-1],d-1)

# Returns number of nodes at depth d        
def NodesAtDepth(T,d):
    if d ==0:
        return len(T.item)
    if T.isLeaf:
        return 0
    else:
        n = 0
        for i in range(len(T.child)):
            n = n + NodesAtDepth(T.child[i],d-1)
    return n   
    
# Prints items at depth d
def PrintAtDepth(T,d):
    if d ==0:
        for t in T.item:
            print(t,end=' ')       
    if not T.isLeaf:
        for i in range(len(T.child)):
            PrintAtDepth(T.child[i],d-1)
            
# Returns number of full nodes    
def FullNodes(T):
    if IsFull(T):
        return 1
    if T.isLeaf:
        return 0
    else:
        n = 0
        for i in range(len(T.child)):
            n = n + FullNodes(T.child[i])
    return n

# Returns number of full leaves
def FullLeaves(T):
    if T.isLeaf:
        if IsFull(T):
            return 1
        else:
            return 0
    else:
        n = 0
        for i in range(len(T.child)):
            n = n + FullLeaves(T.child[i])
    return n

# Finds depth of k, if k not found returns -1
def DepthOfKey(T,k):
    if k in T.item:
        return 0
    if T.isLeaf: #If item not found
        return -1
    if k > T.item[-1]:#Search last branch
        d = DepthOfKey(T.child[-1],k)
    else:#Search rest of tree
        d = -1
        for i in range(len(T.item)):
            if k < T.item[i]:
                d = DepthOfKey(T.child[i],k)
            if d == 0:# if item was found
                break# Stops loop from searching rest of tree
    if d == -1:
        return -1
    return d + 1

L = [30, 50, 10, 20, 60, 70, 100, 40, 90, 80, 110, 120, 1, 11 , 3, 4, 5,105, 115, 200, 2, 45, 6]        
T = BTree()    
for i in L:
    Insert(T,i) 
PrintD(T,'')
print("")

start = time.time()
print("Height:",height(T))
end = time.time()
heightRunTime = end - start

L2 = []
start = time.time()
SortedList(T,L2)
end = time.time()
SortedRunTime = end - start
print("List:",L2)

print("Items at depth",2,":",end=' ')
start = time.time()
PrintAtDepth(T,2)
end = time.time()
printDepthRunTime = end - start

start = time.time()
smallest = MinAtDepth(T,3)
end = time.time()
minRunTime = end-start

start = time.time()
largest = MaxAtDepth(T,3)
end = time.time()
maxRunTime = end - start

start = time.time()
count = NodesAtDepth(T,1)
end = time.time()
depthRunTime = end - start

start = time.time()
full = FullNodes(T)
end = time.time()
FullNodesRunTime = end - start

start = time.time()
fLeaf = FullLeaves(T)
end = time.time()
FullLeavesRunTime = end - start

start = time.time()
kDepth = DepthOfKey(T,105)
end = time.time()
KeyDepthRunTime = end - start

print("")
print("Min:", smallest)
print("Max: ", largest)
print("Nodes at Depth: ", count)
print("Full Nodes: ",full)
print("Full leaves", fLeaf)
print("Key found at Depth: ",kDepth)

print("")
print("Runtimes")
print("Height: ",heightRunTime)
print("SortedList: ",SortedRunTime)
print("Print at Depth: ",printDepthRunTime)
print("Number of nodes at Depth: ",depthRunTime)
print("Min Node at Depth: ",minRunTime)
print("Max Node at Depth: ",maxRunTime)
print("Full Nodes: ",FullNodesRunTime)
print("Full Leaves: ",FullLeavesRunTime)
print("Key at Depth: ",KeyDepthRunTime)