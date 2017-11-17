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
        temp = ts.existsX_func(temp)

        #Xc(x) & #x'(del(x,x')&fj(x'))
        if cFunc != True:
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

        temp = ts.transitionFunction & gen.compose(ts.submap)


        #There exists part #x'(del(x,x')&fj(x'))
        temp = ts.existsX_func(temp)

        #fj+1 = fj & (#x'(del(x,x')&fj(x')))
        ngen = And(gen,temp).simplify()
        #print(ngen)
        if (gen.equivalent(ngen)):# fj+1 ==fj
            break
        gen  = ngen
    return gen

def existsNext(ts,func):
    #checks there exists next (func)
    gen  = func
    #del(x,x') & f(x')( here f is represented by gen)
    temp = ts.transitionFunction & gen.compose(ts.submap)
    #There exists part #x'(del(x,x')&f(x'))
    gen  = Or(temp.compose(ts.zeroNext),temp.compose(ts.oneNext))
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

def findStates(ts,propertyFunction):
    #returns all the states that satisfy propertyFunction
    gen = [i for i in ts.nodes if ((ts.stateFunction[i]&propertyFunction).to_dnf().equivalent(ts.stateFunction[i].to_dnf()))]
    print ("[*]States satisfying property: "+str(gen))
    return gen

def checkProperty(ts,propertyFunction):
    #returns true if ts satisfies property
    states = findStates(ts,propertyFunction)
    res    = True if set(ts.init) < set(states) else False
    print("[*]Given transition system satisfies the property " if res else "[!]Transition system doesnot satisfy the property")
    return (res)
