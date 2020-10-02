import cv2
import sys
import json
from math import isinf
import matplotlib.pyplot as plt
from util.Point import *
# import util.Point
from util.Line import *
from util.rbt import *


# Debug function for lists
def show(L: list):
    n = len(L)
    for i in range(n):
        print(L[i])
    print()

# Plotting points and line
def plot(lines , points=None):
    for i in lines:
        lx = [i.l.x]
        ly = [i.l.y]
        plt.scatter(lx,ly, c='b', label="Left Points")
        rx = [i.r.x]
        ry = [i.r.y]
        plt.scatter(rx,ry, c='g', label="Right Points")
        plt.plot([i.l.x , i.r.x] , [i.l.y , i.r.y] , 'k')
    if points is not None:
        for i in points:
            x = [i.x]
            y = [i.y]
            plt.scatter(x,y, c='r', label="Left Points")

    # plt.legend(loc='upper left')
    plt.show()

# Get Input from Input File
def getInput():
    f = open('Input' , 'r')
    T = json.load(f)
    return T

# Checks collinearity
def on(a,b,c):
    if b.x <= max(a.x , c.x) and b.x >= min(a.x , c.x) and b.y <= max(a.y , c.y) and b.y >= min(a.y , c.y):
        return True
    return False

# -ve is ccw, +ve is cw, 0 is collinear
def ccw(a,b,c):
    # Change to float if error
    d = (b.y - a.y)*(c.x - b.x) - (c.y - b.y)*(b.x - a.x)
    if d == 0:
        return 0
    elif d>0:
        return 1
    elif d<0:
        return -1

# Checks line intersect
def intersect(p1,q1,p2,q2): 
      
    # Find the 4 orientations required for  
    # the general and special cases 
    o1 = ccw(p1, q1, p2) 
    o2 = ccw(p1, q1, q2) 
    o3 = ccw(p2, q2, p1) 
    o4 = ccw(p2, q2, q1) 
  
    # General case 
    if ((o1 != o2) and (o3 != o4)): 
        return True
  
    # p1 , q1 and p2 are colinear and p2 lies on segment p1q1 
    if ((o1 == 0) and on(p1, p2, q1)): 
        return True
  
    # p1 , q1 and q2 are colinear and q2 lies on segment p1q1 
    if ((o2 == 0) and on(p1, q2, q1)): 
        return True
  
    # p2 , q2 and p1 are colinear and p1 lies on segment p2q2 
    if ((o3 == 0) and on(p2, p1, q2)): 
        return True
  
    # p2 , q2 and q1 are colinear and q1 lies on segment p2q2 
    if ((o4 == 0) and on(p2, q1, q2)): 
        return True
    return False

def createLines(Ti):
    L = []
    for i in Ti:
        a = [Point(i[0]) , Point(i[1])]
        a = sorted(sorted(a , key = lambda x: x.y) , key=lambda x: x.x)
        L.append(Line(a[0] , a[1]))
    return L

def coff(L1):
    p1 = [L1.l.x , L1.l.y]
    p2 = [L1.r.x , L1.r.y]
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0]*p2[1] - p2[0]*p1[1])
    return [A, B, -C]

def intersection(L1, L2):
    D  = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return Point([x,y])
    else:
        return False
