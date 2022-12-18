#Tested on Python v3.10.0
#Test was run without error about 35 times
from random import *
from Segtree import *

a = [randrange(0,9) for i in range(50)]
seggs = Segtree(a, lambda x,y: x+y)

#Test query
for i in range(50):
    for j in range(i+1,51):
        s0 = sum(a[i:j])
        s = seggs.query(i,j)
        if s != s0:
            print(f'[L:R] = [{i},{j}] failed')
#Test get
for i in range(-50,50):
    v0 = a[i]
    v = seggs.get(i)
    if v != v0:
        print(f'seggs.get({i}) failed')
#Test update
a_ = [i for i in range(50)]
for i in range(50):
    seggs.update(i, i)
for i in range(50):
    for j in range(i+1,51):
        s0 = sum(a_[i:j])
        s = seggs.query(i,j)
        if s != s0:
            print(f'updated [L:R] = [{i},{j}] failed')
#Test arr
copy = seggs.arr()
for i in range(50):
    if i != copy[i]:
        print(f'Array copy index {i} wrong')
