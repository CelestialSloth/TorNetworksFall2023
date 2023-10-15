import networkx as nx
import matplotlib.pyplot as plt

class AS_node():
    """
    Used to store ASes by their number.
    """
    def __init__(self, ASN):
        self.ASN = ASN 
        self.paths = [] #all paths found with ASN as origin
        self.edges = []
        self.bandwidth = "" #TODO: how to do weight
        self.G = None

    #can add paths and edges to self from string, path
    def addPath(self, path):
        self.paths.append(path)
        p = path.split(" ")
        x = 1
        while(x < len(p)):
            self.edges.append((p[x-1], p[x]))
            x += 1

    """
    Creates a local graph using networkx, for all paths originating from a certain ASN
    """
    def saveGraph(self):
        self.G = nx.Graph() 
        self.G.add_node(self.ASN)
        for x in self.paths:
            listofPaths = x.split(" ")
            self.G.add_nodes_from(listofPaths)
        self.G.add_edges_from(self.edges)
        return 

    #displays self's local graph
    def showLocalGraph(self):
        if self.G == None:
            self.saveGraph()
        nx.draw(self.G, with_labels=True)
        plt.show() 
        return

    #saves self's local graph to file {ASN}.png
    def saveLocalGraph(self):
        if self.G == None:
            self.saveGraph()
        nx.draw(self.G, with_labels=True)
        saveFile = self.ASN + ".png"
        plt.savefig(saveFile)
        plt.close()
        return
    
    def createNodeFromDict(self, AS_dict): #TODO: finish function
        print(AS_dict)
        return 

    """
    Writes the ASN number and it's corresponding paths to a file, r, used in createLocalGraph.py.
    """
    def writeToFile(self, r):
        txt = "{} {}\n".format(self.ASN, self.bandwidth)
        r.write(txt)
        print(txt)

        for x in self.paths:
            #print(x)
            r.write(x)
            r.write("\n")
        r.write("\n")

    def get_BC(self):
        if (self.G == None):
            self.saveGraph()
        v = self.ASN
        G = self.G
        nodeList = []
        totalShortestPaths, pathsWithV = 0, 0

        for x in G.nodes:
            for y in G.nodes:
                if (x != y and x != v and y != v):
                    shortest = nx.all_shortest_paths(G, x, y)
                    #print("From %s to %s: "% (x, y))
                    for r in shortest:
                            if (v in r):
                                pathsWithV += 1
                            totalShortestPaths += 1
                            #print(r)
        print("total paths: %i" % totalShortestPaths)
        print("paths with v: %i" % pathsWithV)
        res = float(pathsWithV) / float(totalShortestPaths)
        return res

def getTiming(month, year):
    start = "%s-%s-01 07:00:00" % (year, str(month).zfill(2))
    end = "%s-%s-02 07:00:00 UTC" % (year, str(month).zfill(2))
    return (start, end)

"""Loops through list of nodes to save to file, r"""
def writeNodes(nodes, r):
    for n in nodes:
        nodes[n].writeToFile(r)

def dumpPickle(data, filename):
    picklefile = open(filename, 'wb+')
    pickle.dump(data, picklefile)
    picklefile.close()

def loadPickle(filename):
    picklefile = open(filename, 'rb')
    data = pickle.load(picklefile)
    picklefile.close()
    return data

def openFile(filename):
    try: 
        f = open(filename, "r")
        return f
    except (OSError, IOError):
        print("Error opening file")
        exit(1)

"""Returns dictionary with all ASes from list as keys"""
def loadASList(listOfAS):
    f = openFile(listOfAS)
    dic = {}
    for l in f:
        dic[l[:-2]] = []
    f.close()
    return dic

def getTestNode():
    node = AS_node("12345")
    node.path = ["123 1435 345"]
    return node
