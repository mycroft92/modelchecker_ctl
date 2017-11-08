from automata import *
from ctl_language import *
from pyeda.inter import *
from time import time


sm1     = {0:[0,1],1:[0]}
l1      = {'a':[1]}
init    = [0]
start   = time()
ts1     = TS(sm1,init,l1,"ts1.dot")

#make property there exists[]a
p1      = existsCUB(ts1,True,label(ts1,'a'))

#check if p1 holds on ts1
print (checkProperty(ts1,p1))
print (findStates(ts1,p1))
elapsed = time() - start
print ("Time elapsed: %.4f s"%elapsed)

#Example 6.1 in book
start   = time()
sm    = {1:[3],2:[1,4],3:[2],4:[2]}
init  = [1]
l     = {'b':[4],'g':[3],'r':[1],'y':[1]}
ts    = TS(sm,init,l,"ts.dot")

#for all future y in enf = Not # global not y
pa    = Not(existsGB(ts,Not(label(ts,'y'))))
print (checkProperty(ts,pa))
print (findStates(ts,pa))

#there exists global not g
pg    = existsGB(ts,Not(label(ts,'g')))
print (checkProperty(ts,pg))
print (findStates(ts,pg))

#for all global g = not(there exists future not g)
pnotg = Not(existsCUB(ts,true(),Not(label(ts,'g'))))
print (checkProperty(ts,pg))
print (findStates(ts,pg))

elapsed = time() - start
print ("Time elapsed: %.4f s"%elapsed)
