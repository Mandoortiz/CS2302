"""
Author: Armando Ortiz
Course: CS 2302 Data Structures
Assignment: Lab 2
Instructor: Olac Fuentes
T.A.: Anindita Nath, Maliheh Zargaran
Last Modification: Feb 26, 2019
Purpose: The purpose of this program is to compare bubble sort, merge sort,
    quicksort, and modified qiucksort to compare their running times.
    This is done using linked lists of differing sizes
"""
import numpy as np
comparisons = 0 # Global variable for counting comparisons

#Node Functions
class Node(object):
    # Constructor
    def __init__(self, item, next=None):  
        self.item = item
        self.next = next 
        
def PrintNodes(N):
    if N != None:
        print(N.item, end=' ')
        PrintNodes(N.next)       

#List Functions
class List(object):   
    # Constructor
    def __init__(self): 
        self.head = None
        self.tail = None
        self.length = 0

def IsEmpty(L): 
    # Checks if List L is empty
    return L.head == None     

def GetLength(L):
    # Finds length of List L
    if IsEmpty(L):
        return 0
    else:
        temp = L.head
        count = 0
        while temp is not None:
            temp = temp.next
            count +=1
        return count

def Append(L,x): 
    # Inserts x at end of list L
    if IsEmpty(L):
        L.head = Node(x)
        L.tail = L.head
    else:
        L.tail.next = Node(x)
        L.tail = L.tail.next
    L.length += 1

def ElementAt(L,n):
    # Finds element at n location for List L
    if IsEmpty(L) or (n>GetLength(L)-1):
        return None
    temp = L.head
    for i in range(n):
        temp = temp.next
    return temp.item

def Print(L):
    # Prints list L's items in order using a loop
    temp = L.head
    while temp is not None:
        print(temp.item, end=' ')
        temp = temp.next
    print()  # New line 
    
def Copy(L):
    # Makes copy of List L
    temp = L.head
    copy = List()
    while temp is not None:
        Append(copy, temp.item)
        temp = temp.next
    return copy

def randomList(n):
    # Creates List of size n using random integers
    L = List()
    for i in range(n):
        Append(L,np.random.randint(1, 101))# Adds random integer to list
    return L

# Sorting Functions    
# Bubble Sort
def bubbleSort(L):
    global comparisons
    tempNode = L.head
    while tempNode is not None:# Iterate through each item on list until done
        t = L.head
        while t.next is not None:# Iterates pass of list
            if t.item > t.next.item:# Compares item to next item in list
                temp = t.next.item
                t.next.item = t.item
                t.item= temp  
            t = t.next
            comparisons = comparisons + 1
        tempNode = tempNode.next

# Merge Sort Functions
# Function for merging the lists
def merge(L,L1,L2):
    global comparisons
    while (L1.head is not None) and (L2.head is not None):# Compare 
        if L1.head.item <= L2.head.item:# Adds L1 item if L1 is smaller
            Append(L,L1.head.item)
            L1.head = L1.head.next
        elif L2.head.item < L1.head.item:# Adds L2 item if L2 is smaller
            Append(L,L2.head.item)
            L2.head = L2.head.next 
        comparisons = comparisons +1
    
    if L1.head is None:# Adds rest of L1 if L2 is empty
        while L2.head is not None:
            Append(L,L2.head.item)
            L2.head = L2.head.next
            comparisons = comparisons + 1
    
    elif L2.head is None:# Adds rest of L2 if L1 is empty
        while L1.head is not None:
            Append(L,L1.head.item)
            L1.head = L1.head.next
            comparisons = comparisons + 1   
    
def mergeSort(L):
    global comparisons
    if GetLength(L) > 1:
        mid = (GetLength(L))//2 # Finds midpoint
        L1 = List()# Left List
        L2 = List()# Right List
        i = 0;
        while L.head is not None:
            if i < mid:# Adds items on list before midpoint
                Append(L1,L.head.item)
            else:# Adds items on list after midpoint
                Append(L2,L.head.item)
            L.head = L.head.next
            i = i + 1
            comparisons = comparisons +1
        
        mergeSort(L1)# Recurrence for left side of list
        mergeSort(L2)# Recurrence for right side of list
        merge(L,L1,L2)# Call to merge lists

# Quicksort Functions
# Function to combine lists
def combine(L,L1,L2):
    global comparisons
    while L1.head is not None:# Adds left half of list
        Append(L,L1.head.item)
        L1.head = L1.head.next
        comparisons = comparisons + 1
    while L2.head is not None:# Adds right side to list
        Append(L,L2.head.item)
        L2.head = L2.head.next
        comparisons = comparisons + 1

# Quicksort Function       
def quickSort(L):
    global comparisons
    if GetLength(L) > 1:
        pivot = L.head.item# Item to compare to rest of list 
        L1=List()# Left List
        L2=List()# Right List
        L.head = L.head.next# List item after Pivot
        
        while L.head is not None:# Move through List
            if L.head.item < pivot:# Items lower than pivot
                Append(L1,L.head.item)
            else:# Rest of the items
                Append(L2,L.head.item)
            comparisons = comparisons + 1
            L.head = L.head.next
        
        quickSort(L1)# Recurrence for left side
        quickSort(L2)# Recurrence for right side
        Append(L1,pivot)# Append pivot to end of Left List
        combine(L,L1,L2)# Call to combine the lists

# Find Median
# Median of Bubble Sorted List
def bubbleMedian(L):
    global comparisons
    C = Copy(L)
    bubbleSort(C)
    print("Bubble Sort",end=' ')
    Print(C)
    return(ElementAt(C,GetLength(C)//2))

# Median of Merge Sorted List
def mergeMedian(L):
    C = Copy(L)
    mergeSort(C)
    print("Merge Sort",end=' ')
    Print(C)
    return(ElementAt(C,GetLength(C)//2))

# Median of Quick Sorted List
def quickMedian(L):
    C = Copy(L)
    quickSort(C)
    print("Quick Sort:",end=' ')
    Print(C)
    return(ElementAt(C,GetLength(C)//2))

# Main
i = 5
while i <= 30:# Loop to test comparisons    
    print("Test Size: ",i)     
    L = randomList(i)
    print("Original L")
    Print(L)
    
    comparisons = 0
    print("Median: ", bubbleMedian(L))
    print("Comparisons",comparisons)
    print("")
    
    comparisons = 0
    print("Median: ", mergeMedian(L))
    print("Comparisons: ",comparisons)
    print("")
    
    comparisons = 0
    print("Median: ", quickMedian(L))
    print("Comparisons: ",comparisons)
    print("")
    print("")
    i = i + 5