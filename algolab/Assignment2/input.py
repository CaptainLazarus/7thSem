import random
import cv2
import sys
import json
from math import isinf
import matplotlib.pyplot as plt

f = open('Input' , 'w')

T = []

for t in range(1):
    L = []
    for i in range(7):
        x,y = random.randint(0,100),random.randint(0,100)
        x1,y1 = random.randint(0,100),random.randint(0,100)
        L.append([(x,y) , (x1,y1)])
    T.append(L)

json.dump(T , f)

f.close()