"""
Author: Armando Ortiz
Course: CS 2302 Data Structures
Assignment: Lab 1
Instructor: Olac Fuentes
T.A.: Anindita Nath, Maliheh Zargaran
Last Modification: Feb 10, 2019
Purpose: The purpose of this program is to recursively draw different figures. 
"""
import numpy as np
import matplotlib.pyplot as plt
import math

#Draw Squares
def draw_squares(ax,n,orig,p,w):
    if n>0:
        q = p*w #Lowers size of square
        
        #Builds Squares
        square1 = q+orig #Top right square
        square2 = q-orig #Bottom left square
        square3 = np.array([[q[0][0]-orig, q[0][1]+orig], #Top left square
                            [q[1][0]-orig, q[1][1]+orig],
                            [q[2][0]-orig,q[2][1]+orig],
                            [q[3][0]-orig, q[3][1]+orig],
                            [q[4][0]-orig,q[4][1]+orig]])
        square4 = np.array([[q[0][0]+orig, q[0][1]-orig], #Bottom right square
                            [q[1][0]+orig, q[1][1]-orig],
                            [q[2][0]+orig,q[2][1]-orig],
                            [q[3][0]+orig, q[3][1]-orig],
                            [q[4][0]+orig,q[4][1]-orig]])
    
        ax.plot(p[:,0], p[:,1], linewidth=1, color='k')#Draws Square
        
        #Recursive calls for squares
        draw_squares(ax,n-1,orig,square1,w) #Top Right
        draw_squares(ax,n-1,orig,square2,w) #Bottom Left
        draw_squares(ax,n-1,orig,square3,w) #Top Left
        draw_squares(ax,n-1,orig,square4,w) #Bottom Right
        

#Draw Tree       
def draw_tree(ax,line,x,y,dely,n):
    if n>0:
        #Builds Branches
        left = [line[0]-x,line[1]-y] #Builds left branch
        right = [line[0]+x,line[1]-y] #Builds right branch
        
        ax.plot([line[0],left[0]],[line[1],left[1]], #Draws left branch 
                [line[0],right[0]],[line[1],right[1]],linewidth=1,color='k') #Draws right branch
        
        #Recursive Calls for branches
        draw_tree(ax,left,x/2,y,dely,n-1) #Left branches
        draw_tree(ax,right,x/2,y,dely,n-1) #Right branches

#Creates Circle      
def circle(cent,rad):
    n = int(4*rad*math.pi)
    t = np.linspace(0,6.3,n)
    x = cent[0]+rad*np.sin(t)
    y = cent[1]+rad*np.cos(t)
    return x, y

#Draws Circles
def draw_circles(ax,n,center,radius,w):
    if n>0:
        x,y = circle(center,radius)
        x = x + radius
        ax.plot(x,y,linewidth=1,color='k')
        draw_circles(ax,n-1,center,radius*w,w)
 
#Draws pattern of circles             
def drawcirclePattern(ax,n,c,r,w):
    if n>0:
        x,y = circle(c,r) #Builds Circle
        ax.plot(x, y, linewidth=1, color='k') #Draws Circle
        
        #Recursive calls for circles
        drawcirclePattern(ax,n-1,c,r*w,w)#Middle circle
        drawcirclePattern(ax,n-1,[(c[0]+r)-(r*w),c[1]],r*w,w) #Right Circle
        drawcirclePattern(ax,n-1,[c[0],(c[1]+r)-(r*w)],r*w,w) #Top Circle
        drawcirclePattern(ax,n-1,[(c[0]-r)+(r*w),c[1]],r*w,w) #Left Circle
        drawcirclePattern(ax,n-1,[c[0],(c[1]-r)+(r*w)],r*w,w) #Bottom Circle
        
#Draw Squares        
orig_size = 1000
mid = np.array([0,0])
square = np.array([[-orig_size,-orig_size], [-orig_size,orig_size], [orig_size,orig_size],[orig_size,-orig_size], [-orig_size,-orig_size]])

#First Square      
plt.close("all") 
fig, ax = plt.subplots()
draw_squares(ax,2,orig_size,square,.5)
ax.set_aspect(1.0)
ax.axis('off')
plt.show()
fig.savefig('square1.png')

#Second Square
plt.close("all") 
fig, ax = plt.subplots()
draw_squares(ax,3,orig_size,square,.5)
ax.set_aspect(1.0)
ax.axis('off')
plt.show()
fig.savefig('square2.png')

#Third Square
plt.close("all") 
fig, ax = plt.subplots()
draw_squares(ax,4,orig_size,square,.5)
ax.set_aspect(1.0)
ax.axis('off')
plt.show()
fig.savefig('square3.png')

#Draw Tree
line = np.array([0,0])
x = 1000
y = 1000

#First Tree
plt.close("all")
fig, ax = plt.subplots()
draw_tree(ax,line,x,y,3,3)
ax.set_aspect(1.0)
ax.axis('off')
plt.show()
fig.savefig('tree1.png')

#Second Tree
plt.close("all")
fig, ax = plt.subplots()
draw_tree(ax,line,x,y,4,4)
ax.set_aspect(1.0)
ax.axis('off')
plt.show()
fig.savefig('tree2.png')

#Third Tree
plt.close("all")
fig, ax = plt.subplots()
draw_tree(ax,line,x,y,7,7)
ax.set_aspect(1.0)
ax.axis('off')
plt.show()
fig.savefig('tree3.png')

#Draw Circles  
#First Circle    
plt.close("all") 
fig, ax = plt.subplots() 
draw_circles(ax, 9, [0,0], 100,.5)
ax.set_aspect(1.0)
ax.axis('off')
plt.show()
fig.savefig('circles1.png')

#Second Circle
plt.close("all") 
fig, ax = plt.subplots() 
draw_circles(ax, 50, [0,0], 100,.9)
ax.set_aspect(1.0)
ax.axis('off')
plt.show()
fig.savefig('circle2.png')

#Third Circle
plt.close("all") 
fig, ax = plt.subplots() 
draw_circles(ax, 100, [0,0], 100,.9)
ax.set_aspect(1.0)
ax.axis('off')
plt.show()
fig.savefig('circles3.png')

#drawCirclePattern
#First Pattern
plt.close("all") 
fig, ax = plt.subplots() 
drawcirclePattern(ax, 3, [0,0], 100,.33)
ax.set_aspect(1.0)
ax.axis('off')
plt.show()
fig.savefig('circlepattern1.png')

#Second Pattern
plt.close("all") 
fig, ax = plt.subplots() 
drawcirclePattern(ax, 4, [0,0], 100,.33)
ax.set_aspect(1.0)
ax.axis('off')
plt.show()
fig.savefig('circlepattern2.png')

#Third Pattern
plt.close("all") 
fig, ax = plt.subplots() 
drawcirclePattern(ax, 5, [0,0], 100,.33)
ax.set_aspect(1.0)
ax.axis('off')
plt.show()
fig.savefig('circlepattern3.png')
