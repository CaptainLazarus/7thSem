from math import isinf

# Line ->  P(x1,y1) ----------------------- Q(x2,y2)
class Line:
    def __init__(self , l , r):
        self.l = l
        self.r = r
        if self.l.x - self.r.x == 0:
            self.m = float('inf')
        else: 
            self.m = (self.l.y - self.r.y)/(self.l.x - self.r.x)
        if isinf(self.m):
            self.c = self.l.x
        else:
            self.c = self.l.y - (self.m*self.l.x)
    
    def getm(self):
        return self.m
    
    def getc(self):
        return self.c

    def __repr__(self):
        return "{} <-> {}".format(self.l , self.r)
