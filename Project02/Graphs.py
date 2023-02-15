import networkx as nx
import Experiment

def read_graph_from_file(filename="Project01/ia-infect-dublin/ia-infect-dublin.mtx"):
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

def _get_graph_nineteenfour_from_NCM_book():
    G = nx.Graph()
    G.add_nodes_from(range(1,16))
    G.add_edges_from([(1,2),(1,3),(2,3),(2,6),(4,5),(4,6),(4,7),(5,7),(5,8),(6,9),(7,8),(7,9),(7,10)])
    G.add_edges_from([(8,10),(8,14),(9,10),(9,11),(10,12),(11,12),(11,15),(12,13),(12,15),(12,16)])
    G.add_edges_from([(13,14),(13,16),(13,17),(14,17),(15,16),(16,17)])
    return G

#Graph from fig 19.4
NCM_Graph = _get_graph_nineteenfour_from_NCM_book()

# circulant graph with 2 neighbors each side
circulantGraph_2x = nx.circulant_graph(20, [1, 2])

# circulant graph with 4 neighbors each side
circulantGraph_4x = nx.circulant_graph(20, [1, 2, 3, 4])

karateGraph = nx.karate_club_graph()

BAGraph_100 = nx.barabasi_albert_graph(100, 2)

BAGraph_410 = nx.barabasi_albert_graph(410, 2)

smallWorldGraph_100 = nx.watts_strogatz_graph(100,5,.3)

smallWorldGraph_410 = nx.watts_strogatz_graph(410,3,.3)

dublinGraph = read_graph_from_file()

Graphs = ['NCM_Graph','circulantGraph_2x','circulantGraph_4x','karateGraph','BAGraph_100','BAGraph_410',
            'smallWorldGraph_100','smallWorldGraph_410','dublinGraph']

# steps = 100
# trials = 10

for G in Graphs:
    E = Experiment(eval(G), steps, trials, G)
    E.run()

