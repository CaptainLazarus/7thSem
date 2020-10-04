import random
import cv2
import json
import argparse

def input():
    parse = argparse.ArgumentParser(description='Input for program')
    parse.add_argument('-t' , type=int , help='Number of test cases')
    parse.add_argument('-n' , type=int , help='Number of line segments')
    parse.add_argument('-r' , type=int , help='Range of point')
    return parse.parse_args()

def generateInput(t , n , r):
    f = open('Input' , 'w')
    T = []
    for _ in range(t):
        L = []
        for _ in range(n):
            x,y = random.randint(0,r),random.randint(0,r)
            x1,y1 = random.randint(0,r),random.randint(0,r)
            L.append([(x,y) , (x1,y1)])
        T.append(L)

    json.dump(T , f)
    f.close()


print("\n[INFO] --- Generating Input\n")
inp = input()
generateInput(inp.t , inp.n , inp.r)