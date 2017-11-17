#Author       : mycroft92
#Date         : 07-Nov-2017
#Description  : Automaton representation class for ctl model checking
#Requirements : Depends on graphviz,pyeda,python3.6
from pyeda.inter import *
import graphviz as gv
import math

class TS(object):
    def __init__(self,stateHash={},initStates=[],labels={},filename="bdd.dot"):
        #stateHash is node to nodelist hash, the list indicates out edges from the key node
        self.stateHash   = stateHash
        #labels is a prop to state list hash Ex: 'a': [0,1]
        self.labels      = labels
        self.init        = initStates
        self.fname       = filename
        self._gen_graph()
        self._gen_label()

    def _gen_charfunction(self):
        self.nVars       = int(math.ceil(math.log(len(self.nodes))))
        self._min        = min(self.nodes)
        self._max        = max(self.nodes)
        self.stateVar    = exprvars('x',self.nVars)
        self.nextVar     = exprvars('x_',self.nVars)
        self.submap      = {}
        self.zeroNext    = {}
        self.oneNext     = {}
        #I created one stateVar for each state

        #substituion map for each variable and making next states all 0 and 1 hashes
        self.submap      = dict(zip(self.stateVar,self.nextVar))
        for i in range (0,self.nVars):
            self.zeroNext[self.nextVar[i]] = False
            self.oneNext[self.nextVar[i]]  = True

        #Creating boolean functions to represent individual states and next states
        self.stateFunction   = {i:True for i in self.nodes}
        self.nextFunction    = {i:True for i in self.nodes}
        for n in self.nodes:
            b                = bin(n-self._min)[2:].zfill(self.nVars)
            for i in  range(0,len(b)):
                temp         = self.stateVar[i] if b[i]=='1' else Not(self.stateVar[i])
                ntemp        = self.nextVar[i] if b[i]=='1' else Not(self.nextVar[i])
                self.stateFunction[n] = And(self.stateFunction[n],temp)
                self.nextFunction[n]  = And(self.nextFunction[n],ntemp)
        #print ("State functions")
        #for i in self.nodes:
        #    print (i,self.stateFunction[i])
        #Transition function generation
        self.transitionFunction = False
        for (x,y) in self.edges:
            self.transitionFunction = self.transitionFunction | (self.stateFunction[x] &self.nextFunction[y])
        self.initFunction     = Or(*[self.stateFunction[i] for i in self.init])

    def existsX_func(self,func):
        out = func
        for i in self.nextVar:
            out  = Or(out.compose({i:False}),out.compose({i:True}))
        return out


    def _gen_label(self):
        self._gen_charfunction()
        self.labelFunctions  = {}
        #print ("Generating label functions")
        for key in self.labels.keys():
            self.labelFunctions[key] = Or(*[self.stateFunction[i] for i in self.labels[key]])

        #    print (key,self.labelFunctions[key])

    def _gen_graph(self):
        node_style = {
        'fontname': 'Helvetica',
        'shape': 'hexagon',
        'fontcolor': 'white',
        'color': 'white',
        'style': 'filled',
        'fillcolor': '#006699'}
        graph_attr = {
        'fontsize': '16',
        'fontcolor': 'white',
        'bgcolor': '#333333',
        'rankdir': 'TB'  }
        self.G  = gv.Digraph(graph_attr=graph_attr,format="svg")
        self.nodes = []
        self.edges = []
        self._dump_graph()
        self.G.save(self.fname)
        return self.G

    def _dump_graph(self):
        node_style = {
        'fontname': 'Helvetica',
        'shape': 'hexagon',
        'fontcolor': 'white',
        'color': 'white',
        'style': 'filled',
        'fillcolor': '#006699'}
        edge_solid = {
        'style': 'solid',
        'color': 'blue',
        'arrowhead': 'empty',
        'dir'  : 'forward',
        'fontname': 'Courier',
        'fontsize': '12',
        'fontcolor': 'black'   }
        for key in self.stateHash.keys():
            if not(key in self.nodes):
                self.G.node(str(key),_attributes=node_style)
                self.nodes.append(key)
            for v in self.stateHash[key]:
                if not(v in self.nodes):
                    self.G.node(str(v),_attributes=node_style)
                    self.nodes.append(v)
                if not ((key,v) in self.edges):
                    self.G.edge(str(key),str(v),_attributes=edge_solid)
                    self.edges.append((key,v))

if __name__ == "__main__":
    sm = {0:[0,1],1:[0]}
    ts = TS(sm)
