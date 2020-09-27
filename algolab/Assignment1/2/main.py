import cv2
import matplotlib.pyplot as plt
from collections import deque 
from math import atan2
import random
import time

#Debug
def ishow(x):
    cv2.imshow('Img' , x)
    cv2.waitKey(0)

def show(L):
    n = len(L)
    # print(n)
    for i in range(10):
        print(L[i])
    print()

# Plotting points/hull
def plot(points, hull=None , type=0):
	if type == 0:
		X = [x[0] for x in points]
		Y = [x[1] for x in points]
		plt.scatter(X, Y, c='b', label="Points")
		
		if hull is not None:
			X1 = [x[0] for x in hull]
			Y1 = [x[1] for x in hull]
			plt.scatter(X1, Y1, c='r', label="Hull")
			plt.plot(X1 , Y1)
			# plt.plot(X1[0] , Y1[0])
			plt.plot((X1[0] , X1[-1]) , (Y1[0] , Y1[-1]) , c='b')

		# plt.legend(loc='upper left')
		# plt.show()
	if type == 1:
		X = [x[0] for x in points]
		Y = [x[1] for x in points]
		plt.scatter(X, Y, c='b', label="Points")
		
		if hull is not None:
			for i in hull:
				p1,p2 = i[0],i[1]
				X1 = [p1[0] , p2[0]]
				Y1 = [p1[1] , p2[1]]
				plt.scatter(X1, Y1, c='r', label="Hull")
				plt.plot((p1[0] , p2[0]) , (p1[1] , p2[1]) , c='b')
		# plt.show()

#Graham Scan
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
	hull = [anchor, P_polar[0]]
	for s in P_polar[1:]:
		while det(hull[-2], hull[-1], s) <= 0:
			del hull[-1] # backtrack
			if len(hull)<2: break
		hull.append(s)
	return hull

#Bruteforce. Lel. Fails Miserably.
def bruteForce(points):
	#Brute Force
	def det(p1, p2, p3):
			return ((p2[0]-p1[0])*(p3[1]-p1[1]) - (p3[0]-p1[0])*(p2[1]-p1[1]))

	hull = []

	for i in points:
		for j in points:
			flag = 1
			if i != j:
				for k in points:
					if k != i and k != j:
						if det(i,j,k) > 0:
							flag = 0
				if flag == 1:
					hull.append((i,j))
					# hull.append(j)
	return hull

#Output
def output(img , hull):
	n = len(hull)
	for i in range(n):
		print(hull[i] , hull[(i+1)%n])
		cv2.line(img, hull[i] , hull[(i+1)%n] , (0,0,255) , 2)
	cv2.imwrite('out.jpeg', img) 

#Reading Image
img = cv2.imread('1.jpeg')
grey = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
# ishow(grey)

h,w = grey.shape
print(grey.shape , h , w)

P = []

#Converting Image matrix to points
for i in range(0,w):
    for j in range(0,h):
		# VERY IMP. This determines the cutoff value of the color. Varies between 0-255
		# Putting it at 255 looks unnatural. So 10 it is. Hull changes based on this.
        if grey[j][i] < 10:
            P.append((i,j))

H = graham(P)
print(H)
# plot(P , H)
output(img.copy() , H)