""" Practice with partitioning on an assortative network.
    Create an assortative network.
    Check out its properties by looking at a dendorgram.
    Find its communities using the Louvain algorithm.
    Repeate using Girvan-Newman betweenness
    
Michael A. Goodrich
July 2022, March 2023
Brigham Young University
"""

#from scipy.sparse import csr_matrix
from GraphManager import *

def main():
    myGraphHandler = graphHandler()
    myGraphHandler.showGraph()
    myGraphHandler.showDendrogram()
    
    # Partition using the Louvain method and show network. 
    partition_list = myGraphHandler.getAgentColors_from_LouvainCommunities()
    myGraphHandler.showGraph(title = "Louvain partition for the assortative graph",agent_colors=partition_list)
    
    # Partition using the Girvan Newman method and show network.
    color_map, communities = myGraphHandler.getAgentColors_from_GirvanNewmanCommunities()
    myGraphHandler.showGraph(title = "Girvan-Newman partition for the assortative graph",agent_colors=color_map,wait_for_button=True)
    
main()