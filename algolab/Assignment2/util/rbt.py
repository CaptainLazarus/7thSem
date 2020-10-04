import cv2
import sys
import json
from math import isinf
from util.Util import ccw
from util.Point import *
from util.Line import *
import matplotlib.pyplot as plt
# import matplotlib.animation as 

# Node for Tree
class Node():
    def __init__(self, data):
        self.data = data
        self.parent = None
        self.left = None
        self.right = None
        self.color = 1
    
    def __repr__(self):
        return "({})".format(self.data)

class RedBlackTree():
    def __init__(self):
        self.TNULL = Node(0)
        self.TNULL.color = 0
        self.TNULL.left = None
        self.TNULL.right = None
        self.root = self.TNULL

    # Preorder
    def pre_order_helper(self, node):
        if node != TNULL:
            sys.stdout.write(node.data + " ")
            self.pre_order_helper(node.left)
            self.pre_order_helper(node.right)

    # Inorder
    def in_order_helper(self, node):
        if node != self.TNULL:
            self.in_order_helper(node.left)
            sys.stdout.write(str(node.data) + "\n")
            self.in_order_helper(node.right)

    # Postorder
    def post_order_helper(self, node):
        if node != TNULL:
            self.post_order_helper(node.left)
            self.post_order_helper(node.right)
            sys.stdout.write(node.data + " ")

    # Balancing the tree after deletion
    def delete_fix(self, x):
        while x != self.root and x.color == 0:
            if x == x.parent.left:
                s = x.parent.right
                if s.color == 1:
                    s.color = 0
                    x.parent.color = 1
                    self.left_rotate(x.parent)
                    s = x.parent.right

                if s.left.color == 0 and s.right.color == 0:
                    s.color = 1
                    x = x.parent
                else:
                    if s.right.color == 0:
                        s.left.color = 0
                        s.color = 1
                        self.right_rotate(s)
                        s = x.parent.right

                    s.color = x.parent.color
                    x.parent.color = 0
                    s.right.color = 0
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == 1:
                    s.color = 0
                    x.parent.color = 1
                    self.right_rotate(x.parent)
                    s = x.parent.left

                if s.right.color == 0 and s.right.color == 0:
                    s.color = 1
                    x = x.parent
                else:
                    if s.left.color == 0:
                        s.right.color = 0
                        s.color = 1
                        self.left_rotate(s)
                        s = x.parent.left

                    s.color = x.parent.color
                    x.parent.color = 0
                    s.left.color = 0
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = 0

    def __rb_transplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    # Node deletion
    def delete_node_helper(self, node, line , key):
        z = self.TNULL
        while node != self.TNULL:
            if node.data == line:
                z = node
                break

            result = node.data.m * key.x + node.data.c
            diff = round(result - key.y , 4)

            if diff > 0:
                node = node.left
            elif diff < 0:
                node = node.right
            elif diff == 0:
                if ccw(line.l , key , node.data.l) == -1:
                    node = node.left
                else:
                    node = node.right                    

        if z == self.TNULL:
            print("Cannot find key in the tree")
            return

        y = z
        y_original_color = y.color
        if z.left == self.TNULL:
            x = z.right
            self.__rb_transplant(z, z.right)
        elif (z.right == self.TNULL):
            x = z.left
            self.__rb_transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.__rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.__rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == 0:
            self.delete_fix(x)

    # Balance the tree after insertion
    def fix_insert(self, k):
        while k.parent.color == 1:
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right

                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = 0

    # Printing the tree
    def __print_helper(self, node, indent, last):
        if node != self.TNULL:
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("U----")
                indent += "     "
            else:
                sys.stdout.write("B----")
                indent += "|    "

            s_color = "RED" if node.color == 1 else "BLACK"
            print(str(node.data) + "(" + s_color + ")")
            self.__print_helper(node.left, indent, False)
            self.__print_helper(node.right, indent, True)

    def preorder(self):
        self.pre_order_helper(self.root)

    def inorder(self):
        self.in_order_helper(self.root)

    def postorder(self):
        self.post_order_helper(self.root)

    # Search the tree
    def search_tree_helper(self, node, line , key):
        if line == node.data:
            return node

        # if node == self.TNULL:
        #     return node.parent

        result = node.data.m * key.x + node.data.c
        # result2 = key.m * x + key.c
        # diff = (round(result , 4) - round(result2 , 4))
        diff = round(result - key.y , 4)


        if diff > 0:
            return self.search_tree_helper(node.left, line , key)
        elif diff < 0:
            return self.search_tree_helper(node.right, line , key)
        elif diff == 0:
            if ccw(line.l , key , node.data.l) == -1:
                return self.search_tree_helper(node.left , line , key)
            else:
                return self.search_tree_helper(node.right , line , key)

    def searchTree(self, L , P):
        # print(type(e))
        return self.search_tree_helper(self.root, L , P)

    def minimum(self, node):
        while node.left != self.TNULL:
            node = node.left
        return node

    def maximum(self, node):
        while node.right != self.TNULL:
            node = node.right
        return node

    def successor(self, x):
        if (x.right != self.TNULL):
            return self.minimum(x.right)

        y = x.parent

        if y is None:
            return None

        while y is not None and y != self.TNULL and x == y.right:
            x = y
            y = y.parent
        return y

    def predecessor(self,  x):
        if (x.left != self.TNULL):
            return self.maximum(x.left)

        y = x.parent

        if y is None:
            return None

        # print(y , type(y))
        while y is not None and y != self.TNULL and x == y.left:
            x = y
            y = y.parent
        return y

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    # Key -> (Line , X = K -> For sorting)
    # Insert accordingly. VERY IMP
    def insert(self, line , key):
        node = Node(line)
        node.parent = None
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = 1

        y = None
        x = self.root

        # Heres how you're inserting. 
        # Find intersection of line and all nodes.
        # Binary search tree according to that.
        # If equal, implies intersection point. 
        # At this point, check the x axis of the line and the node.
        # The one with nearer x axis is assumed to be the one above,

        while x != self.TNULL:
            y = x
            
            result = (x.data.m * key.x) + x.data.c
            diff = round(result - key.y , 4)

            # Might have error
            if diff > 0:
                x = x.left
            elif diff < 0:
                x = x.right
            elif diff == 0:
                if ccw(node.data.l , key , x.data.l) == -1:
                    x = x.left
                else:
                    x = x.right

        node.parent = y

        if y is not None:
            result = (y.data.m * key.x) + y.data.c
            diff = round(result - key.y , 4)            

        if y == None:
            self.root = node
        elif diff > 0:
            y.left = node
        elif diff < 0:
            y.right = node
        elif diff == 0:
            if node.data.l.y < y.data.l.y:
                y.left = node
            else:
                y.right = node

        if node.parent == None:
            node.color = 0
            return

        if node.parent.parent == None:
            return

        self.fix_insert(node)

    def swap_helper(self , node , line1 , line2 , key):
        a = self.searchTree(line1 , key)
        b = self.searchTree(line2 , key)

        a.data , b.data = b.data , a.data

        while a.parent is not None:
            a = a.parent
        self.root = a
        return self.root

    def swap(self , line1 , line2 , key):
        self.root = self.swap_helper(self.root , line1 , line2 , key)
        return self.root

    def get_root(self):
        return self.root

    def delete_node(self, line , key):
        self.delete_node_helper(self.root, line , key)

    def print_tree(self):
        # print(self.root)
        self.__print_helper(self.root, "", True)
