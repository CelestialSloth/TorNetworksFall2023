import networkx as nx
import matplotlib.pyplot as plt
from helpers.AS_nodes import AS_node

"""Given a path, ListE, it write each path between two nodes as tuples"""
def getEdges(ListE):
    edges = []
    for x in range (0, len(ListE) - 1):
        edges.append((ListE[x], ListE[x+1]))
    return edges

"""creates graph with only AS paths from the same origin AS. 
ARGV:
    takes filename to read data, can have multiple graphs
"""
def createLocalGraph(filename):
    try:
        f = open(filename, "r")
    except (OSError, IOError):
        print("Can't open file given to createGlobalGraph()")
        exit(1)

    for l in f: #going line by line
        if l == '\n': #at a new line, it's a new graph
            nx.draw(G, with_labels=True)
            plt.savefig(figName)
            plt.show()
            continue 
        s = l.split(" ")
        print(s)
        if len(s) == 1: #The ASN will be on it's own line
            G = nx.Graph()
            G.add_node(l)
            figName = "Graph_%s" % l
        else: #keep reading paths
            s = l.split(" ")
            e = getEdges(s)
            G.add_nodes_from(s)
            G.add_edges_from(e)
    #TODO: make graph for each AS 
    f.close()
    plt.show()
    return

#global graph made of all reported AS paths regardless of origin AS and prefix
#get this file from self.writeToFile() in AS_nodes.py
"""
Loops through each node and adds them and all nodes from their paths into one graph.
ARGV:
    dictionary of AS_nodes
"""
def createGlobalGraph(nodes):
    G = nx.Graph() 
    for n in nodes:
        G.add_node(n.ASN)
        for p in n.paths:
            G.add_nodes_from(p)
        G.add_edges_from(n.edges)
    nx.draw(G, with_labels=True)
    plt.savefig("globalGraph")

"""
Creates a global graph from basic file with ASN followed by paths.
ARGV:
    filename: text file name
"""
def createGlobalGraphFile(filename):
    try:
        f = open(filename, "r")
    except (OSError, IOError):
        print("Can't open file given to createGlobalGraph()")
        exit(1)
    G = nx.Graph()

    for l in f:
        if l == '\n':
            continue 
        s = l.split(" ")
        if len(s) == 1: #The ASN
            print(l)
            G.add_node(l)
        else: #the paths
            e = getEdges(s)
            G.add_nodes_from(s)
            G.add_edges_from(e)
    
    nx.draw(G, with_labels=True)
    plt.savefig("globalGraph")
    plt.show()
    f.close()
    return

def main():
    #createLocalGraph("streamTestResults-2022-06")
    createGlobalGraph("streamTestResults-2022-06")

if __name__ == "__main__":
    main()