import time
import json
import functools
from math import atan2
import matplotlib.pyplot as plt
import random
import numpy as np


class Line:
    def __init__(self, point1, point2):
        """A simple linear line"""
        self.point1 = point1
        self.point2 = point2
        # work out y = mx + c
        self.x1, self.y1 = point1
        self.x2, self.y2 = point2
        self.m = (self.y1-self.y2) / (self.x1-self.x2)
        self.c = self.y1 - self.m * self.x1
    
    def distance_from(self, x, y):
        """Work out the distance of the y co-ordinates for simplicity"""
        line_y = self.m*x + self.c
        return y - line_y
    
    def intersects(self, line):
        """Work out whether this line intersects another line"""
        if self.m == line.m or np.any(np.in1d(self.points, line.points)):
            return False # If the gradients are the same or the line edges are the same
        A = np.array([[-self.m, 1], [-line.m, 1]])
        b = np.array([self.c, line.c])
        x, y = np.linalg.solve(A, b) # Solve for x and y


        # If the lines intersect then the intersection point should be in range of the line's y co-ordinates
        top_point_y = max(self.points, key=lambda x: x[1])[1]
        bot_point_y = min(self.points, key=lambda x: x[1])[1]

        return bot_point_y < y < top_point_y
    
    def plot(self, **kwargs):
        """A method to plot the line for simplicity"""
        import matplotlib.pyplot as plt
        plt.plot([self.x1, self.x2], [self.y1, self.y2], **kwargs)

    @property
    def midpoint(self):
        """Returns the midpoint of the line"""
        xs = np.array([self.x1, self.x2])
        ys = np.array([self.y1, self.y2])
        return np.array([np.mean(xs), np.mean(ys)])

    @property
    def points(self):
        return np.array([self.point1, self.point2])
class ConvexPolygon:
    """A polygon object which may only be convex"""
    def __init__(self, *lines):
        self.lines = lines
        self.x = True
        self.vertices = np.unique([np.array(p) for l in self.lines for p in l.points], axis=0)
        
    def surrounds(self, point):
        """Check if the polygon surrounds a given point"""
        point = np.array(point)
        furthest_vertex = max(self.vertices, key=lambda x: np.linalg.norm(x-point))
        line = Line(furthest_vertex, point)
        return not any(line.intersects(x) for x in self.lines)

    def plot(self):
        """Plot the polygon for simplicity"""
        import matplotlib.pyplot as plt
        for l in self.lines:
            l.plot(color='r')
    
    @property
    def sides(self):
        """Returns the number of sides the polygon has"""
        return len(self.lines)
def convex_hull(points, plot=False):
    start_time = time.time()

    # points = np.random.randn(npoints*2).reshape(npoints,2) # Generate 250 random co-ordinates
    print(points)
    if plot:
        plt.scatter(points.T[0], points.T[1], s=10) # Display all the points

    min_x = points[np.argmin(points.T[0])]
    max_x = points[np.argmax(points.T[0])]
    line = Line(min_x, max_x) 
    max_y = max(points, key=lambda x: line.distance_from(*x))
    min_y = min(points, key=lambda x: line.distance_from(*x))

    # Collect all the lines and create a polygon object from them
    lines = [Line(min_x, max_y), Line(max_y, max_x), Line(max_x, min_y), Line(min_y, min_x)]
    poly = ConvexPolygon(*lines)

    def points_outside(polygon):
        """Used to filter through a numpy array to get only the points which lie outside the polygon"""
        return np.invert(np.apply_along_axis(polygon.surrounds, 1, points))

    def direct_point_function(polygon, line):
        """Used to filter through a numpy array to get only the points which are in direct view of a side of a polygon"""
        check_list = list(polygon.lines)
        check_list.remove(line)
        def is_direct_point(point):
            l = Line(point, line.midpoint)
            return not any(l.intersects(test_line) for test_line in check_list)
        return is_direct_point

    points = points[points_outside(poly)]
    while points.size > 0: 
        new_polygon_sides = []
        for line in poly.lines:
            is_direct_point = direct_point_function(poly, line)
            x = np.apply_along_axis(is_direct_point, 1, points)
            line_points = points[x]
            
            if not line_points.size:
                new_polygon_sides.append(line)
                continue
            
            furthest_point = max(line_points, key=lambda x: abs(line.distance_from(*x)))
            new_polygon_sides.append(Line(line.point1, furthest_point))
            new_polygon_sides.append(Line(line.point2, furthest_point))
        poly = ConvexPolygon(*new_polygon_sides)
        points = points[points_outside(poly)]

    time_taken = time.time() - start_time

    print("Generated a {} sided convex hull to contain {} points".format(poly.sides, len(points)))
    print("Time taken: {}s".format(time_taken))
    
    if plot:
        poly.plot()
        plt.show()
    
    return time_taken

def input(n , p):
    f = open('Input' , 'w')
    T = []
    for t in range(n):
        P = []
        for i in range(p):
            x,y = random.randint(0,500),random.randint(0,500)
            # print(x,y)
            P.append((x,y))
        T.append(P)
    json.dump(T , f)
    f.close()

#Graph
def make_graph(graham,bruteForce,divide , x_label , y_label):
    X = [x[0] for x in graham]
    Y = [x[1] for x in graham]
    plt.scatter(X, Y, c='g', label="Graham")

    X = [x[0] for x in bruteForce]
    Y = [x[1] for x in bruteForce]
    plt.scatter(X, Y, c='b', label="Brute Force")

    X = [x[0] for x in divide]
    Y = [x[1] for x in divide]

    plt.scatter(X, Y, c='r', label="Divide and Conquer")
    plt.legend(loc='upper left')


    scale_factor = 1
    xmin, xmax = plt.xlim()
    ymin, ymax = plt.ylim()
    # plt.xlim(xmin * scale_factor, xmax * scale_factor)
    plt.ylim(ymin * scale_factor, ymax * scale_factor)

    plt.xlabel(x_label)
    plt.ylabel(y_label)

    # plt.legend(loc='upper left')
    plt.show()

# Debug func
def show(L: list):
    n = len(L)
    # print(n)
    for i in range(10):
        print(L[i])
    print()

# Plotting points/hull
# def cop(a,b):
#     if a[0] == b[0] and a[1] == b[1]:
#         return 1 

def plot(points, hull=None, type=0):
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

        # plt.legend(loc='upper left')
        plt.show()
    if type == 1:
        X = [x[0] for x in points]
        Y = [x[1] for x in points]
        plt.scatter(X, Y, c='b', label="Points")

        if hull is not None:
            for i in hull:
                p1, p2 = i[0], i[1]
                X1 = [p1[0], p2[0]]
                Y1 = [p1[1], p2[1]]
                plt.scatter(X1, Y1, c='r', label="Hull")
                plt.plot((p1[0], p2[0]), (p1[1], p2[1]), c='b')
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

#Bruteforce approach
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
                        if det(i, j, k) > 0:
                            flag = 0
                if flag == 1:
                    hull.append((i, j))
                    # hull.append(j)
    return hull

'''
T = List of 10 inputs (temp 5) -> List of 1000 points (temp 10) -> (xi,yj)
'''

#Time vs Input Size
timesG = []
timesB = []
timesD = []

#Output size vs Input Size
timesG1 = []
timesB1 = []

#Running Time vs Output Size
timesG2 = []
timesB2 = []

# ZZ -> Test Cases
for zz in range(1,10):
    # Points generated randomly between 1-100
    input(1,100)

    f = open("Input", 'r')
    T = json.load(f)

    # for i in range(len(T)):
    #     T1 = np.array(T[i])
    #     start_time = time.time()
    #     time_taken = convex_hull(T1)
    #     timesD.append((zz*10 , time_taken))

    #Running graham for all test cases
    for i in range(len(T)):
        start_time = time.time()
        H = graham(T[i])
        time_taken = time.time() - start_time
        print("Time taken: {}s".format(time_taken))
        timesG.append((zz*10 , time_taken))
        timesG1.append((zz*10 , len(H)))
        timesG2.append((len(H) , time_taken))
        # Uncomment to see convex hull
        # plot(T[i],hull=H)

    #Running brute force for all test cases
    for i in range(len(T)):
        start_time = time.time()
        H = bruteForce(T[i])
        time_taken = time.time() - start_time
        print("Time taken: {}s".format(time_taken))
        timesB.append((zz*10 , time_taken))
        timesB1.append((zz*10 , len(H)))
        timesB2.append((len(H) , time_taken))
        # Uncomment to see convex hull
        # plot(T[i] , hull=H , type=1)
        
make_graph(timesG , timesB , timesD , 'input' , 'time')
make_graph(timesG1 , [] , [] , 'input' , 'output')
make_graph([] , timesB1 , [] , 'input' , 'output')
make_graph(timesG2 , timesB2 , [] , 'output' , 'time')