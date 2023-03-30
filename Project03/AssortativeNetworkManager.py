""" Create a graph using the algorithm following equations 1 and 2 
from https://arxiv.org/pdf/cond-mat/0210146

Newman, Mark EJ, and Michelle Girvan. 
"Mixing patterns and community structure in networks." 
Statistical mechanics of complex networks. 
Springer, Berlin, Heidelberg, 2003. 66-87.

Implementation by Mike Goodrich
Brigham Young University
February 2022
"""

import networkx as nx
import numpy as np


class MixedNetworkFormation:
    def __init__(self, color_template=None):
        ### Initialize Algorithm with four types using Equation 3 ###
        self.blue = 0
        self.magenta = 1
        self.cyan = 2
        self.green = 3
        self.color_template = color_template
        # self.typeList = [self.blue, self.magenta, self.cyan, self.green]
        num_types = 4
        # self.typeList = self.typeList[:num_types]
        self.typeList = list(range(num_types))
        assert len(self.typeList) == num_types
        # more weakly assortative
        self.Eij = np.array(
            [
                [0.18, 0.02, 0.01, 0.03],
                [0.02, 0.20, 0.03, 0.02],
                [0.01, 0.03, 0.16, 0.01],
                [0.03, 0.02, 0.01, 0.22],
            ]
        )  # Mixing matrix
        # more strongly assortative
        self.Eij = np.array(
            [
                [0.4, 0.02, 0.01, 0.03],
                [0.02, 0.4, 0.03, 0.02],
                [0.01, 0.03, 0.4, 0.01],
                [0.03, 0.02, 0.01, 0.4],
            ]
        )  # Mixing matrix
        # six types
        # self.Eij = np.array(
        # [
        # [0.4, 0.02, 0.01, 0.03, 0.01, 0.03],
        # [0.02, 0.4, 0.03, 0.02, 0.02, 0.02],
        # [0.01, 0.03, 0.4, 0.01, 0.01, 0.03],
        # [0.03, 0.02, 0.01, 0.4, 0.03, 0.01],
        # [0.01, 0.01, 0.01, 0.03, 0.4, 0.02],
        # [0.03, 0.02, 0.03, 0.01, 0.02, 0.4],
        # ]
        # )  # Mixing matrix
        self.G = nx.Graph()

        # Run the algorithm
        self._AlgorithmStep1()
        self._AlgorithmStep2()
        self._AlgorithmStep3()
        self._AlgorithmStep4()

        ### Set graph properties ###
        self.color_map = self._getColorMap()

    """ Public methods """

    def getGraph(self):
        return self.G

    def getGroundTruthColors(self):
        return self.color_map

    def getColorTemplate(self):
        return self.color_template

    """ Private methods """
    ### Graph Helpers
    def _getColorMap(self):
        color_map = []
        for node in self.G.nodes:
            if self.G.nodes[node]["type"] == self.blue:
                color_map.append(self.color_template[0])
            elif self.G.nodes[node]["type"] == self.cyan:
                color_map.append(self.color_template[1])
            elif self.G.nodes[node]["type"] == self.magenta:
                color_map.append(self.color_template[2])
            else:
                color_map.append(self.color_template[3])
        return color_map

    ### Algorithm Step 1 ###
    def _AlgorithmStep1(self):
        self.PoissonLambda = 5

    ### Algorithm Step 2 ###
    def _AlgorithmStep2(self):
        self.numEdges = 200  # This is how many edges I want
        self.edgeNumbersDict = self._drawEdgesFromMixingMatrix()
        self.endsByTypeDict = self._countEndsOfEdgesByType()
        self.expectedNumberOfNodes = self._computeExpectedNumberOfNodes()

    def _drawEdgesFromMixingMatrix(self):
        edgeNumbersDict = dict()
        # initialize dictionary
        for type1 in self.typeList:
            for type2 in self.typeList:
                if type2 >= type1:
                    edgeNumbersDict[(type1, type2)] = 0
        count = 0
        while count < self.numEdges:
            for type1 in self.typeList:
                for type2 in self.typeList:
                    if np.random.uniform(low=0.0, high=1.0) < self.Eij[type1][type2]:
                        if type2 >= type1:
                            edgeNumbersDict[(type1, type2)] += 1
                        else:
                            edgeNumbersDict[(type2, type1)] += 1
                        count += 1
        # (edgeNumbersDict)
        # print("There are ", sum([edgeNumbersDict[key] for key in edgeNumbersDict.keys()])," edges in the dictionary")
        return edgeNumbersDict

    def _countEndsOfEdgesByType(self):
        endsByTypeDict = {k: 0 for k in self.typeList}  # initialize dictionary
        for type1 in self.typeList:
            for type2 in self.typeList:
                if type2 < type1:
                    continue
                if type1 == type2:
                    endsByTypeDict[type1] += self.edgeNumbersDict[(type1, type2)] * 2
                else:
                    endsByTypeDict[type1] += self.edgeNumbersDict[(type1, type2)]
                    endsByTypeDict[type2] += self.edgeNumbersDict[(type1, type2)]
        # print("node ends by type ", endsByTypeDict)
        return endsByTypeDict

    def _computeExpectedNumberOfNodes(self):
        numNodeDict = dict()
        for type in self.typeList:
            n = np.round(self.endsByTypeDict[type] / self.PoissonLambda)
            # print(int(n))
            numNodeDict[type] = int(n)
        return numNodeDict

    ### Algorithm Step 3 ###
    def _AlgorithmStep3(self):
        self.nodeListByTypeAndDegree = self._drawNodesFromTypes()

    def _drawNodesFromTypes(self):
        nodesByDegreeDict = {
            k: [] for k in self.typeList
        }  # initialize to dictionary of empty lists
        for type in self.typeList:
            nodeList = self._drawNodesByType(type)
            nodesByDegreeDict[type] = nodeList
        # print("nodesByDegreeDict = ", nodesByDegreeDict)
        return nodesByDegreeDict

    def _drawNodesByType(self, type):
        nodeList = list()
        # print("Trying to get ", self.endsByTypeDict[type]," total degrees")
        while len(nodeList) != self.expectedNumberOfNodes[type]:
            if len(nodeList) < self.expectedNumberOfNodes[type]:
                node = np.random.poisson(lam=self.PoissonLambda)
                if node == 0:
                    continue
                nodeList.append(node)
            # print("Number of nodes in node set ", type, " is ", sum(nodeList))
            if len(nodeList) > self.expectedNumberOfNodes[type]:
                nodeList.pop(0)
                # print("Number of nodes in node set ", type, " is ", sum(nodeList))
        # print("Length of nodeList for type ",type, " = ",len(nodeList))
        return nodeList

    ### Algorithm Step 4 ###
    def _AlgorithmStep4(self):
        self._addNodesToGraph()
        self._addEdgesToGraph()  # Requires nodes to be added to graph

    def _addNodesToGraph(self):
        # Make the node list into a a format with node_id by type
        nodeList = []
        nodeID = 0
        for type in self.typeList:
            for nodeDegree in self.nodeListByTypeAndDegree[type]:
                nodeList.append((nodeID, {"type": type, "degree": nodeDegree}))
                nodeID += 1
        # print("node list is ", nodeList)
        self.G.add_nodes_from(nodeList)
        return nodeList

    def _addEdgesToGraph(self):
        # print("Adding edges to graph")
        for edge_type in self.edgeNumbersDict.keys():
            type1 = edge_type[0]
            type2 = edge_type[1]
            while self.edgeNumbersDict[edge_type] > 0:
                free_agents1 = self._getFreeAgents(type1)
                free_agents2 = self._getFreeAgents(type2)
                if free_agents1 == [] or free_agents2 == []:
                    break
                node1 = free_agents1[np.random.randint(0, len(free_agents1))]
                neighbors_of_node = [n for n in self.G[node1]]
                neighbors_of_node.append(node1)  # If same type, don't allow self loops
                possible_neighbors = list(set(free_agents2) - set(neighbors_of_node))
                if possible_neighbors == []:
                    break
                index2 = np.random.randint(0, high=len(possible_neighbors))
                node2 = possible_neighbors[index2]
                self.G.add_edge(node1, node2)
                self.edgeNumbersDict[edge_type] -= 1
                self._decrementRemainingDegree(node1)
                self._decrementRemainingDegree(node2)
        # print("Done adding edges to graph")
        return

    def _getFreeAgents(self, type):
        # return agents of specified type that have free stubs
        # print("Graph node info is ", self.G.nodes.data())
        nodes = []
        for node in self.G.nodes.data():
            node_info = list(node)
            node_index = node_info[0]
            node_degree = node_info[1]["degree"]
            node_type = node_info[1]["type"]
            if node_type == type and node_degree > 0:
                nodes.append(node_index)
        return nodes

    def _decrementRemainingDegree(self, node_index):
        # subtract one from the nodeList
        self.G.nodes[node_index]["degree"] -= 1
        # print("node ", node_index, " now has remaining degree ", self.G.nodes[node_index]['degree'], "\n\n")
        return
