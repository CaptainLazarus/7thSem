import random
import json

f = open('Input' , 'w')

T = []

for t in range(10):
    P = []
    for i in range(1000):
        x,y = random.randint(0,500),random.randint(0,500)
        # print(x,y)
        P.append((x,y))
    T.append(P)

json.dump(T , f)

f.close()