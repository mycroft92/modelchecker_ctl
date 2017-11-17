from automata import *
from ctl_language import *
from pyeda.inter import *
from time import time

#state 0 - n1,n2,y=1 -->idle1,idle2
#state 1 - w1,n2,y=1 -->entering1,idle2
#state 2 - n1,w2,y=1 -->idle1,entering2
#state 3 - c1,n2,y=0 -->critical1,idle2
#state 4 - w1,w2,y=1 -->entering1,entering2
#state 5 - n1,c2,y=0 -->idle1,critical2
#state 6 - c1,w2,y=0 -->critical1,entering2
#state 7 - w1,c2,y=0 -->entering1,critical2

sm1     = {0:[1,2],1:[3,4],2:[4,5],3:[0,6],4:[6,7],5:[0,7],6:[2],7:[1]}
lab     = {'idle1':[0,2,5],'idle2':[0,1,3],'entering1':[1,4,7],'entering2':[2,4,6],'critical1':[3,6],'critical2':[5,7]}
init    = [0]
start   = time()
ts1     = TS(sm1,init,lab,"mutex.dot")

#AG(entering1 > AF critical1) == not EF not(entering1 -> AF critical1)
# == not EF (entering1 and EG (not critical1))

EGnC    = existsGB(ts1,Not(label(ts1,'critical1')))
print ("Not critical1")
findStates(ts1,Not(label(ts1,'critical1')))
print ("Exists global not critical1")
findStates(ts1,EGnC)
ENEC    = And(label(ts1,'entering1'),EGnC)
print("Entering and global not critical1")
findStates(ts1,ENEC)
print ("State satisfying AG(enterin1 -> AF critical1)")
prop    = Not(existsCUB(ts1,True,ENEC))
print   (checkProperty(ts1,prop))
findStates(ts1,prop)
elapsed = time() - start
print ("Time elapsed: %.4f s"%elapsed)
