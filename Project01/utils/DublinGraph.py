import numpy as np
import networkx as nx

class DublinGraph:

    def _read_graph_from_file(filename="ia-infect-dublin/ia-infect-dublin.mtx"):
        fo = open(filename,"r")
        line = fo.readline() # Read file header
        line = fo.readline() # Number of vertices and edges
        if not line:
            print("error -- illegal format for input")
            return
        v = line.split(" ")
        numVertices = int(v[0])
        G = nx.Graph()
        G.add_nodes_from(range(1, numVertices+1))
        while True:
            line = fo.readline()
            if not line:
                break
            #print("Line{}: {}".format(count,line.strip()))
            v = line.split(" ")
            v1 = int(v[0])
            v2 = int(v[1])
            G.add_edge(v1,v2)
            G.add_edge(v2,v1)
        fo.close()
        return G