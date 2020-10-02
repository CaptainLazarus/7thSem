# Point -> (x,y)
class Point:
    def __init__(self, P):
        self.x = P[0]
        self.y = P[1]

    def __repr__(self):
        return "({},{})".format(self.x , self.y)

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False
