import cv2
import sys
import json
from math import isinf
import matplotlib.pyplot as plt
from util.Util import *
from util.Point import Point
from util.Line import *
from util.rbt import *

def sweep(L):
    # Insert Function
    def insertQ(p , data):
        # t = []
        if len(p) == 0:
            p.append(data)
            return p
        else:
            i=0
            while data[0].x > p[i][0].x:
                i+=1
                if i == len(p):
                    p.append(data)
                    return p

            if data[0].x == p[i][0].x:
                while data[0].y > p[i][0].y and data[0].x == p[i][0].x:
                    i+=1
                    if i == len(p):
                        p.append(data)
                        return p
            
            p.insert(i , data)
            return p

    Out = []
    P = []
    count = 0
    for i in L:
        insertQ(P , [i.l , i , 0])
        insertQ(P , [i.r , i , 1])
        count+=1

    # for i in P:
    #     print(i)
    
    T = RedBlackTree()

    while len(P) > 0:
        N = P.pop(0)
        if N[2] == 0:
            T.insert(N[0] , N[1])
            c = T.searchTree(N[1])
            p = T.predecessor(c)
            s = T.successor(c)

            if p is not None:
                if intersect(p.data.l , p.data.r , c.data.l , c.data.r):
                    IP = intersection(coff(p.data) , coff(c.data))
                    # print(IP)
                    Out.append(IP)
                    insertQ(P , [IP , [p.data , c.data] , 2])
            if s is not None:
                if intersect(c.data.l , c.data.r , s.data.l , s.data.r):
                    IP = intersection(coff(c.data) , coff(s.data))
                    Out.append(IP)
                    # print(IP)
                    insertQ(P , [IP , [c.data , s.data] , 2])

        elif N[2] == 1:
            T.delete_node(N[1])

        elif N[2] == 2:
            print(IP)
            # print(N[1])
            c1 = T.searchTree(N[1][0])
            p1 = T.predecessor(c1)
            s1 = T.successor(c1)

            c2 = T.searchTree(N[1][1])
            p2 = T.predecessor(c2)
            s2 = T.successor(c2)
            
            # Case 1 -> c1 with p2.
            if p2 is not None:
                if intersect(p2.data.l , p2.data.r , c1.data.l , c1.data.r):
                    IP = intersection(coff(p2.data) , coff(c1.data))
                    # print(IP)
                    if IP is not False:
                        if IP.x > N[0].x or IP.x == N[0].x and IP.y > N[0].y:
                            Out.append(IP)
                            insertQ(P , [IP , [p2.data , c1.data] , 2])
            
            # Case 2 -> c1 with s2
            if s2 is not None:
                if intersect(c1.data.l , c1.data.r , s2.data.l , s2.data.r):
                    IP = intersection(coff(c1.data) , coff(s2.data))
                    if IP is not False:
                        if IP.x > N[0].x or IP.x == N[0].x and IP.y > N[0].y:
                            Out.append(IP)
                            # print(IP)
                            insertQ(P , [IP , [c1.data , s2.data] , 2])

            # Case 1 -> c2 with p1.
            if p1 is not None:
                if intersect(p1.data.l , p1.data.r , c2.data.l , c2.data.r):
                    IP = intersection(coff(p1.data) , coff(c2.data))
                    if IP is not False:
                        if IP.x > N[0].x or IP.x == N[0].x and IP.y > N[0].y:
                            # print(IP)
                            Out.append(IP)
                            insertQ(P , [IP , [p1.data , c2.data] , 2])
            
            # Case 2 -> c2 with s1
            if s1 is not None:
                if intersect(c2.data.l , c2.data.r , s1.data.l , s1.data.r):
                    IP = intersection(coff(c2.data) , coff(s1.data))
                    if IP is not False:
                        if IP.x > N[0].x or IP.x == N[0].x and IP.y > N[0].y:
                            Out.append(IP)
                            # print(IP)
                            insertQ(P , [IP , [c2.data , s1.data] , 2])

            T.swap(N[1][0] , N[1][1])
            # T.delete_node(N[1])
            # T.insert()

    return Out
    # T.print_tree()

if __name__ == "__main__":
    
    Point([1,2])
    # print(intersect(Point([1,2]) , Point([2,3]) , Point([1,3]) , Point([2,2])))
    print("\n[INFO] --- Getting Input\n")
    T = getInput()

    # tree = RedBlackTree()
    # l1 = Line(Point([1,1]) , Point([3,3]))
    # l2 = Line(Point([1,3]) , Point([3,1]))
    # l3 = Line(Point([1,4]) , Point([4,5]))
    # l4 = Line(Point([0,1]) , Point([0,4]))

    # tree.insert(l1)
    # tree.insert(l2)
    # tree.insert(l3)
    # tree.insert(l4)

    # # tree.swap(l1 , l2)
    # tree.print_tree()
    
    # ith Test case
    for i in range(len(T)):
        # print(T[i])
        
    #     print("\n[INFO] --- Creating Lines\n")
        L = createLines(T[i])
        # show(L)
        
        # print("\n[INFO] --- PLotting Lines\n")
        # plot(L)

        print("\n[INFO] --- Starting Sweep\n")
        I = sweep(L)
        print(I)
        plot(L , I)

# CPU times. -> 100x