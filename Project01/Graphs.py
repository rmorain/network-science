import networkx as nx
import Experiment

def read_graph_from_file(filename="ia-infect-dublin/ia-infect-dublin.mtx"):
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

# circulant graph with 2 neighbors each side
circulantGraph_2x = nx.circulant_graph(20, [1, 2])

# circulant graph with 4 neighbors each side
circulantGraph_4x = nx.circulant_graph(20, [1, 2, 3, 4])

completeGraph_100 = nx.complete_graph(100)

latticeGraph_100 = nx.grid_2d_graph(10, 10)

BAGraph_100 = nx.barabasi_albert_graph(100, 3)

BAGraph_410 = nx.barabasi_albert_graph(410, 3)

dublinGraph = read_graph_from_file()

Graphs = ['circulantGraph_2x','circulantGraph_4x','completeGraph_100','latticeGraph_100','BAGraph_100',
            'BAGraph_410','dublinGraph']

steps = 100
trials = 10

for G in Graphs:
    E = Experiment(eval(G), steps, trials, G)
    E.run()

