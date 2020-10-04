import cv2
import sys
import json
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

    # ith Test case
    for i in range(len(T)):

        print("\n[INFO] --- Processing Input\n")
        L = createLines(T[i])
        
        print("\n[INFO] --- PLotting Lines\n")
        plot(L)

        print("\n[INFO] --- Starting Sweep\n")
        I = sweep(L)
        # print(I)

        print("\n[INFO] --- Plotting Intersection Points\n")
        plot(L , I)
