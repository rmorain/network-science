""" Graph Handler method. Creates and manages an assortative graph.

Michael A. Goodrich
Brigham Young University
July 2022 """

import matplotlib as mpl
#mpl.use('tkagg')
from matplotlib import pyplot as plt
import networkx as nx
from ComputeAndPlotDendrogram import *
from scipy.cluster.hierarchy import dendrogram
import community as community_louvain
#import networkx.algorithms.community as nx_comm
from networkx.algorithms.community.centrality import girvan_newman

from AssortativeNetworkManager import *

class graphHandler:
    def __init__(self):
        self.figureNumber = 1
        self.myNetwork = MixedNetworkFormation(color_template=['b', 'm', 'c', 'y', 'r', 'c', 'g'])
        self.G = self.myNetwork.getGraph()
        self.color_template = self.myNetwork.getColorTemplate()
        self.color_map = self.myNetwork.getGroundTruthColors()
        self.pos = nx.nx_agraph.graphviz_layout(self.G,prog='neato')
        self.title = 'Assortative graph with ' + str(len(self.G.nodes)) + ' agents'

        #print(self.G.nodes())
    """ Public Methods"""
    def showGraph(self,agent_colors = None,figureNumber = None,wait_for_button = False ,title = None):
        if agent_colors == None: agent_colors = self.color_map
        if figureNumber == None: figureNumber = self.figureNumber; self.figureNumber += 1
        if title == None: title = self.title
        plt.figure(figureNumber);plt.clf()
        plt.ion()
        ax = plt.gca()
        ax.set_title(title)
        nx.draw(self.G,self.pos,node_color = agent_colors, node_size = 70, alpha=0.8)
        if wait_for_button == True: plt.waitforbuttonpress()
        else: plt.waitforbuttonpress(0.05)
    def updateGraph(self,agent_colors = None,wait_for_button = False ,title = None):
        if agent_colors == None: agent_colors = self.color_map
        if title == None: title = self.title
        ax = plt.gca()
        ax.set_title(title)
        nx.draw_networkx_nodes(self.G,self.pos,node_color = agent_colors, node_size = 70)
        if wait_for_button == True: plt.waitforbuttonpress()
        else: plt.waitforbuttonpress(0.2)
    def showDendrogram(self,figureNumber = None,wait_for_button = False):
        if figureNumber == None: figureNumber = self.figureNumber; self.figureNumber += 1
        myHandler = DendrogramHandler(self.G)
        Z = myHandler.getLinkMatrix()
        ZLabels = myHandler.getLinkMatrixLabels()
        plt.figure(figureNumber);plt.clf()
        dendrogram(Z, labels=ZLabels)
        if wait_for_button == True: plt.waitforbuttonpress()
        else: plt.waitforbuttonpress(0.001)
        del myHandler
    def getAdjacencyMatrix(self):
        """ Return the adjacency matrix for the graph as a sparse scipy matrix """
        return nx.adj_matrix(self.G)

    """" Public community detection algorithms """
    def getAgentColors_from_LouvainCommunities(self):
        """ Use the Louvain partition method to break the graph into communities """
        # Louvain method pip install python-louvain
        # see https://arxiv.org/pdf/0803.0476.pdf
        # see https://github.com/taynaud/python-louvain
        color_map = self.color_map
        partition = community_louvain.best_partition(self.G)
        #partition = nx_comm.louvain_communities(self.G)
        #print(partition)
        #print(len(partition))
        #print('there are ',len(partition), ' partitions')
        for node in partition:
            val = partition.get(node)
            color_map[node-1] = self.color_template[val%len(self.color_template)]
        return color_map
    def getAgentColors_from_GirvanNewmanCommunities(self,numPartitions = 4):
        """ Use the Girvan Newman betweeness-based algorithm to partition graph """
        # https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.community.centrality.girvan_newman.html#networkx.algorithms.community.centrality.girvan_newman
        comp = girvan_newman(self.G)
        communities = self._getCommunityWith_N_Partitions(comp,numPartitions)
        color_map = self._getColorMapFromCommunities(communities)
        return color_map, communities

    """ Private methods """
    def _getCommunityWith_N_Partitions(self,all_communities,numPartitions):
        for com in all_communities:
            if len(list(com)) == numPartitions:
                communities = list(com)
                break
        return communities
    def _getColorMapFromCommunities(self,communities):
        color_map = self.color_map
        partition_number = 0
        for partition in communities: 
            #print("***\n",partition)
            for node in partition:
                color_map[node] = self.color_template[partition_number%len(self.color_template)]
            partition_number += 1
        return color_map
        