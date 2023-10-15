import networkx as nx
import matplotlib.pyplot as plt
from kafka.AS_nodes import *

"""Given a list of nodes and a node (v) it returns the betweeness centrality of v

"""
def BC_eq(nodes, node):
    v = node.ASN
    G = node.G
    e = nx.betweenness_centrality(G)
    return e

#TODO:Finish AH, need bandwidth
def AH(e):
    #TODO: how to get rid of biased viewpoints
    n = len(e)
    print("n (# viewpoints) = %i", n)
    sum = 0
    for key in e:
        sum += e[key]
        print(e[key])
    print("Sum found: ", sum)
    #a = ratio of disregarded viewpoints
    #disregard top viewpoints w/ highest num of paths/lowest num
    #BC(j)(V) = BC values computer w/ only viewpoint j

    #give more weight to paths with higher bandwidth


nodes = []
node = AS_node(1)
path = [6,4,1]
node.addPath(path)
path = [6,1]
node.addPath(path)
path = [3,1]
node.addPath(path)
nodes.append(node)

node = AS_node(3)
nodes.append(node)
path = [1,2,3]
node.addPath(path)
path = [6,3]
node.addPath(path)
path = [2,6,3]
node.addPath(path)
path = [6,4,3]
node.addPath(path)
path = [8,3]
node.addPath(path)

node.get_BC()