from pyeda.inter import *

def true():
    return True

def false():
    return False

def  existsCUB(ts,cFunc,bFunc):
    gen   = bFunc
    while True:
        #del(x,x') & fj(x')( here fj is represented by gen)
        temp = And(gen.compose(ts.submap) , ts.transitionFunction)
        #There exists #x'(del(x,x')&fj(x'))
        temp = Or(temp.compose(ts.zeroNext),temp.compose(ts.oneNext))

        #Xc(x) & #x'(del(x,x')&fj(x'))
        temp = And(cFunc,temp)
        #fj+1 = fj | (Xc(x) & #x'(del(x,x')&fj(x')))
        ngen = Or(gen,temp)
        if (gen.equivalent(ngen)): #fj+1 ==fj
            break
        gen  = ngen

    return gen


def existsGB(ts,bFunc):
    gen   = bFunc
    while True:
        #del(x,x') & fj(x')( here fj is represented by gen)
        print(gen.compose(ts.submap))
        temp = ts.transitionFunction & gen.compose(ts.submap)

        #There exists part #x'(del(x,x')&fj(x'))
        temp = Or(temp.compose(ts.zeroNext),temp.compose(ts.oneNext))

        #fj+1 = fj & (#x'(del(x,x')&fj(x')))
        ngen = And(gen,temp).simplify()
        #print(ngen)
        if (gen.equivalent(ngen)):# fj+1 ==fj
            break
        gen  = ngen
    return gen

def implies(ts,aFunc,bFunc):
    gen = Or(Not(aFunc),bFunc)
    return gen

def label(ts,_label):
    assert(type(_label)==type(""))
    try:
        return ts.labelFunctions[_label]
    except KeyError as e:
        print ("[!]The label "+_label+" doesnot appear in labels of given transition system. Please recheck!")
        raise (e)

def checkProperty(ts,propertyFunction):
    #returns true if ts satisfies property
    res = True if implies(ts,ts.initFunction,propertyFunction) else False
    print("[*]Given transition system satisfies the property " if res else "")
    return (res)

def findStates(ts,propertyFunction):
    #returns all the states that satisfy propertyFunction
    gen = [i for i in ts.nodes if (implies(ts,ts.stateFunction[i],propertyFunction))]
    print ("[*]States satisfying property: "+str(gen))
    return gen
