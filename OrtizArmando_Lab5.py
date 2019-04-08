#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Armando Ortiz
Course: CS 2302 Data Structures
Assignment: Lab 4
Instructor: Olac Fuentes
T.A.: Anindita Nath, Maliheh Zargaran
Last Modification: March 24, 2019
Purpose: Takes glove text file of words and embeddings and places them in a Binary Search Tree
 - Prints the number of nodes in the tree
 - Prints height of tree
 - Takes another text file with list of words and returns similarities of the word's embeddings
 - Provides running times of BST construction and word comparisons
"""
import numpy as np
import time

# Class Function
class BST(object):
    # Constructor
    def __init__(self, item, left=None, right=None):  
        self.item = item
        self.left = left 
        self.right = right      
        
# BST Functions
# Inserts item into BST
def Insert(T,newItem):
    if T is None:
        T =  BST(newItem)
    elif T.item[0] > newItem[0]:#Compares words
        T.left = Insert(T.left,newItem)
    else:
        T.right = Insert(T.right,newItem)
    return T

def Find(T,k):
    # Returns the address of k in BST, or None if k is not in the tree
    if T is None:
        return None
    if T.item[0] == k: #Finds word
        return T.item
    if T.item[0]<k:
        return Find(T.right,k)
    return Find(T.left,k)

#Creates BST out of list   
def createBST(T,f):
    for line in f:#While reading file
        if line[0].isalpha():#If word starts with alphabet letter
            spl = line.split(" ")#Splits line into list
            a = np.array(([spl[1:]]))#Creates array for word embeddings
            arr = a.astype(np.float)#Parses embeddings to float numbers
            T = Insert(T,[str(spl[0]),arr])#Places word in BST
    return T

# Compares similarities of embeddings of words
def sim(e0,e1):
    dot = np.sum(e0*e1) #Calculates dot matrix
    mag = np.sqrt(np.sum(np.power(e0,2))) * np.sqrt(np.sum(np.power(e1,2)))#Calculates magnitude
    return round(dot/mag,4)#Returns rounded number to 4th decimal.

# Finds words and sends them to sim method
def compareBST(T,j,k):
    w0 = Find(T,j)#Find word j
    w1 = Find(T,k)#Find word k
    if w0 is None or w1 is None:#If word not found
        return None
    else:
        return sim(w0[1],w1[1])#send to similarities function

# Counts number of nodes in the BST
def countNodes(T):
    if T is None:
        return 0
    return 1 + countNodes(T.left) + countNodes(T.right)

# Finds the hight of the BST
def Height(T):
    if T is None:
        return 0
    else:
        left = Height(T.left)
        right = Height(T.right)
    if left > right:
        return left + 1
    else:
        return right+1


T = None
print("Reading word file to build tree")
try:
    f = open('glove.6B.50d.txt',encoding='utf-8')#Open Text File
except:#If file is not found
    print("File not found")
    f.close()

else:
    print("Building Binary Search Tree")
    print("")
    
    start = time.time()
    T = createBST(T,f)
    end = time.time()
    f.close()
    BSTruntime = end - start
    
    nodes = countNodes(T)
    print("Number of nodes:",nodes)
    height = Height(T)
    print("Height:",height)
    print("Running time for binary search tree construction:", BSTruntime)
    
    print()
    print("Reading word file to find similarities")
    try:
        fl = open('listwords.txt',encoding='utf-8')#List of words for comparison
    except:#If file not found
        print("File not Found")
        fl.close()
    else:
        print("Word similarities found")
        start = time.time()
        for line in fl:
            spl = line.split(" ")
            try:
                spl[1] = spl[1].strip('\n')#Removes new line embedding
                c = compareBST(T,spl[0],spl[1])
                end = time.time()
            except:
                print("Comparison not possible")
            else:
                print("Similarity",spl, "=",c)
                
        BSTCompTime = end - start
        print("Running time for binary search tree query processing:",BSTCompTime)
        fl.close()
