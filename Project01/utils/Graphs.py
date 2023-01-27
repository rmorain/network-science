import networkx as nx
import matplotlib as mpl
mpl.use('tkagg')
from matplotlib import pyplot as plt
from DublinGraph import DublinGraph
import graphviz

#circulant graph with 2 neighbors each side
nx.circulant_graph(20,[1,2]) 

#circulant graph with 4 neighbors each side
nx.circulant_graph(20,[1,2,3,4]) 

nx.complete_graph(100)

nx.grid_2d_graph(10,10)

nx.barabasi_albert_graph(100,3)

nx.barabasi_albert_graph(410,3)

dublinGraph = DublinGraph._read_graph_from_file()

plt.clf()
plt.figure(1);plt.ion()
nx.draw(dublinGraph, node_size=8)
pos = nx.nx_agraph.graphviz_layout(dublinGraph,prog='neato')
plt.waitforbuttonpress()
