import cv2
import sys
import json
import time
from math import isinf
import matplotlib.pyplot as plt
from util.Util import *
from util.Point import Point
from util.Line import *
from util.rbt import *
from util.Sweep import sweep

import argparse


if __name__ == "__main__":

    print("\n[INFO] --- Getting Input\n")
    T = getInput()

    Time = []

    # ith Test case
    for i in range(len(T)):

        print("\n[INFO] --- Processing Input\n")
        L = createLines(T[i])
        
        print("\n[INFO] --- PLotting Lines\n")
        plot(L)

        print("\n[INFO] --- Starting Sweep\n")
        start_time = time.time()
        I = sweep(L)
        time_taken = time.time() - start_time
        Time.append(time_taken)
        # print(I)

        print("\n[INFO] --- Plotting Intersection Points\n")
        plot(L , I)
        # plotTime()