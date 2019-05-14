"""
Author: Armando Ortiz
Course: CS 2302 Data Structures
Assignment: Lab 8
Instructor: Olac Fuentes
T.A.: Anindita Nath, Maliheh Zargaran
Last Modification: May 13, 2019
Purpose: The purpose of this program is to use algorithm design techniques to perform two functions
 - Use Random algorithms to determine the equalities of Trigonometric identities within a list
 - Use Backtracking to partition two sublists with equal sums from the same list.
"""
import random
import math
from mpmath import *
import numpy as np
import time

#Determines equality of both identities
def equal(f1, f2,tries=1000,tolerance=0.0001):
    for i in range(tries):
        t = random.uniform(-math.pi,math.pi)#Picks a random number between -pi and pi
        y1 = eval(f1)
        y2 = eval(f2)
        if np.abs(y1-y2)>tolerance:
            return False
    return True

#Goes through list of Identities to test their quality
def comparisons(eq):
    for i in range(len(eq)):
        for j in range(len(eq)):
            if i != j: #Avoid Duplicates
                if equal(eq[i],eq[j]):
                    print(eq[i],"=",eq[j]) 

#Creates subset list that adds up to goal number
def subsetsum(S,last,goal):
    if goal ==0:
        return True, []
    if goal<0 or last<0:
        return False, []
    res, subset = subsetsum(S,last-1,goal-S[last]) # Take S[last]
    if res:
        subset.append(S[last])
        return True, subset
    else:
        return subsetsum(S,last-1,goal) # Don't take S[last]

#Takes list and creates two partitions with equal sums
def Partition(S):
    total = sum(S)
    S2 = S.copy()
    if total % 2 == 0:#Sublist with two equal partitions not possible if total is odd
        a,s = subsetsum(S,len(S)-1,total//2)
        if a:
            for j in range(len(s)):
                S2.remove(s[j])#Remove items from subset list 
            if sum(S2) == sum(s):#Compare totals of list
                print("Partition Exists")
                print('S1:',s, '= S2:',S2)
            else:
                print('No Partition Exists')
    else:
        print('No Partition Exists')

print("Trigonometric Equalities")    
eq = ['sin(t)','cos(t)','tan(t)','-sin(t)','-cos(t)','-tan(t)','sec(t)','sin(-t)','cos(-t)','tan(-t)','sin(t)/cos(t)','2*sin(t/2)*cos(t/2)','sin(t)*sin(t)','1-cos(t)*cos(t)','(1-cos(2*t))/2','1/cos(t)']
start = time.time()
comparisons(eq)
end = time.time()
comparisonRT = end - start
print("")
print("Comparison Runtime:",comparisonRT)
print("")

S = []
print("Equal Subsets")
start = time.time()
for i in range(10):
    S.append(i)
    print('S:',S)
    Partition(S)
    print("")
end = time.time()
partitionRT = end - start
print("Partition Runtime:",partitionRT)
