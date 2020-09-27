import time
import json
import functools
from math import atan2
import matplotlib.pyplot as plt

# Debug func
def show(L: list):
    n = len(L)
    # print(n)
    for i in range(10):
        print(L[i])
    print()

# Plotting points/hull
def plot(points, hull=None, type=0 , hull2=None):
    if type == 0:
        X = [x[0] for x in points]
        Y = [x[1] for x in points]
        plt.scatter(X, Y, c='b', label="Points")

        if hull is not None:
            X1 = [x[0] for x in hull]
            Y1 = [x[1] for x in hull]
            plt.scatter(X1, Y1, c='r', label="Hull")
            plt.plot(X1, Y1)
            # plt.plot(X1[0] , Y1[0])
            plt.plot((X1[0], X1[-1]), (Y1[0], Y1[-1]), c='b')
        plt.show()
    if type == 1:
        X = [x[0] for x in points]
        Y = [x[1] for x in points]
        plt.scatter(X, Y, c='b', label="Points")

        if hull is not None:
            X1 = [x[0] for x in hull]
            Y1 = [x[1] for x in hull]
            plt.scatter(X1, Y1, c='r', label="Hull")
            plt.plot(X1, Y1 , c='r' , linestyle='dashed')
            # plt.plot(X1[0] , Y1[0])
            plt.plot((X1[0], X1[-1]), (Y1[0], Y1[-1]), c='r' , linestyle='dashed')
        
        if hull2 is not None:
            X1 = [x[0] for x in hull2]
            Y1 = [x[1] for x in hull2]
            plt.scatter(X1, Y1, c='r', label="Hull")
            plt.plot(X1, Y1)
            # plt.plot(X1[0] , Y1[0])
            plt.plot((X1[0], X1[-1]), (Y1[0], Y1[-1]), c='b')
        plt.show()

# Graham Func
def graham(points):
    # Graham
    P = sorted(sorted(points, key=lambda x: x[0]), key=lambda x: x[1])
    anchor = P[0]
    del P[P.index(anchor)]

    def polar(p1, p2=None):
        if p2 == None:
            p2 = anchor
        y = p1[1]-p2[1]
        x = p1[0]-p2[0]
        return atan2(y, x)

    def distance(p1, p2=None):
        if p2 == None:
            p2 = anchor
        y = p1[1]-p2[1]
        x = p1[0]-p2[0]
        return y**2 + x**2

    def det(p1, p2, p3):
        return ((p2[0]-p1[0])*(p3[1]-p1[1]) - (p3[0]-p1[0])*(p2[1]-p1[1]))

    # Main
    P_polar = sorted(sorted(P, key=distance), key=polar)
    # show(P_polar)
    hull = [anchor, P_polar[0]]
    for s in P_polar[1:]:
        while det(hull[-2], hull[-1], s) <= 0:
            del hull[-1]  # backtrack
            if len(hull) < 2:
                break
        hull.append(s)
        # if True: scatter_plot(points,hull)
    return hull

#Assumption -> Input is vertices of polygon given in order (CCW) starting with leftmost point
if __name__ == "__main__":
    a = [[0,0] , [5,0] , [6,1] , [3,2] , [7,5] , [2,3] , [0,5] , [1,2]]
    H = graham(a)
    
    count=0
    j=0
    i=0
    flag = 0

    # Finding pockets comparing convex hull and given vertices
    while j < len(H):
        # print(i,j)
        if a[i] == H[j]:
            i+=1
            j+=1
            if flag == 1:
                flag = 0
                count+=1
        else:
            i+=1
            if flag == 0:
                flag = 1
                count+=1
    # print(i,j)
    if i < len(a):
        count+=1
    if count%2 == 0:
        n = count//2
    else:
        n = count//2 + 1
    print("Number of pockets is {}".format(n))
    plot(a,H,1,a)