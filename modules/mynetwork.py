
##### import modules     #####
import networkx as nx
import numpy as np
from scipy import stats
import random
import sys
##############################

##### matplotlib setting #####
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['font.family']       = 'sans-serif'
mpl.rcParams['font.sans-serif']   = ["Helvetica","Arial","DejaVu Sans","Lucida Grande","Verdana"]
mpl.rcParams['figure.figsize']    = [3,3]
mpl.rcParams['font.size']         = 10
mpl.rcParams["axes.labelcolor"]   = "#000000"
mpl.rcParams["axes.linewidth"]    = 1.0 
mpl.rcParams["xtick.major.width"] = 1.0
mpl.rcParams["ytick.major.width"] = 1.0
cmap1 = plt.cm.tab10
cmap2 = plt.cm.Set3  
colors1 = [cmap1(i) for i in range(0,10)]
colors2 = [cmap2(i) for i in range(0,12)] 
##############################

def compress_nodes(Graph, list_of_node_sets, header="", ):
    # list_of_node_sets=[{'name':name,'node_list':[str1,str2,...]},...]
    
    # enumerate nodes and edges
    node_list=[]; edge_list=[]
    for i, node_set1 in enumerate(list_of_node_sets):
        node_list.append(node_set1['name'])
        for node_set2 in list_of_node_sets[i+1:]:
            connected=False
            for node1 in list(node_set1['set']):
                for node2 in list(node_set2['set']):
                    if node1 == node2:
                        connected=True
                    if Graph.has_edge(node1, node2):
                        connected=True
            if(connected):
                edge_list.append((node_set1['name'], node_set2['name']))
    
    # create networkX network
    G = nx.Graph() # undirected
    G.add_nodes_from(node_list)
    G.add_edges_from(edge_list)
    return G

def overlap_network(list_of_sets, header="", form='exclusive'):
    # enumerate nodes and edges
    node_list=[]; edge_list=[]
    for i, node_set in enumerate(list_of_sets):
        node_list.append(node_set['name'])

    for i, node_set1 in enumerate(list_of_sets):

        # show progress
        if (i%10==0): 
            print("Detecting overlap... "            +
                  str(i) + " / " + str(len(list_of_sets)) ,
                  file=sys.stderr                         )

        for node_set2 in list_of_sets[i+1:]:
            if(form=='exclusive'):
                if(len(node_set1['set'] & node_set2['set'])==0):
                    edge_list.append((node_set1['name'],node_set2['name']))

    # create networkX network
    G = nx.Graph() # undirected
    G.add_nodes_from(node_list)
    G.add_edges_from(edge_list)
    return G

def edge_intersection(Graph_list, header=""):

    G = nx.Graph() # undirected
    
    # get union of node sets of given graphs
    for g in Graph_list:    
        G.add_nodes_from(g.nodes)
    
    # get intersection of edge sets of given graphs
    G.add_edges_from(Graph_list[0].edges)
    for g in Graph_list[1:]:
        g.add_nodes_from(G.nodes)
        G = nx.intersection(G, g)
    
    return G

def cooccurence_network(list_of_sets, universal_set=None, header="", p_threshold=0.05, form='cooccurence'):
    # define universal set if not specified
    universal_set = set()
    for S in list_of_sets:
        universal_set=universal_set | S['set'] # universal set is defined as the union of all sets as default

    # enumerate nodes and edges
    node_list=[]; edge_list=[]
    
    for i, node_set in enumerate(list_of_sets):
        node_list.append(node_set['name'])
    
    for i, node_set1 in enumerate(list_of_sets):
        
        # show progress
        if (i%10==0): 
            print("Detecting co-occurence... "            +
                  str(i) + " / " + str(len(list_of_sets)) ,
                  file=sys.stderr                         )

        for node_set2 in list_of_sets[i+1:]:
            set1=node_set1['set']; comp_set1=universal_set-set1 
            set2=node_set2['set']; comp_set2=universal_set-set2 
            data = np.array([[len(set1 & set2),len(set1 & comp_set2)],
                             [len(comp_set1 & set2),len(comp_set1 & comp_set2)]])
            
            if(form=="cooccurence"):        alternative='greater'
            elif(form=="anti-cooccurence"): alternative='less'

            _, p = stats.fisher_exact(data, alternative='greater'); test="fisher"
            if(p<p_threshold):
                edge_list.append((node_set1['name'],node_set2['name']))
    
    # create networkX network
    G = nx.Graph() # undirected
    G.add_nodes_from(node_list)
    G.add_edges_from(edge_list)
    return G

def max_connected_components_of_random_network(N_edges, ref_Graph=None):
    if(ref_Graph!=None):
        nodes=list(ref_Graph.nodes)
        edges=list(ref_Graph.edges)
        newG=nx.Graph()
        newG.add_edges_from(random.sample(list(ref_Graph.edges),N_edges))
        return max([len(comp.edges()) for comp in nx.connected_component_subgraphs(newG)]) # max edge number

def get_null_dist_of_max_connected_components_of_random_network(N_edges, N_sampling, threshold=None, ref_Graph=None, header=""):
    if(ref_Graph!=None):
        null_dist=[]
        for _ in range(N_sampling):
            null_dist.append(max_connected_components_of_random_network(N_edges, ref_Graph))
        
    # calculate pvalue
    if(threshold!=None):
        count = 0
        for x in null_dist:
            if(x >= threshold): count+=1
        print("p value: "+str(count/len(null_dist))) # one-sided: test if threshold is significantly high value or not

    # plot
    fig = plt.figure(figsize=(2,2))
    ax = fig.add_axes([0.1,0.1,0.8,0.8])
    ax.hist(null_dist,range=(0, N_edges),histtype="step",density=True, rwidth=1, bins=N_edges+1)
    ax.set_xlim(-0.5,N_edges+0.5)
    ax.set_xlabel('# connected edges')
    ax.set_ylabel('Ratio')
    plt.savefig(header+"null_dist.pdf",bbox_inches='tight')

def count_edges_based_on_node_labels(G, node_to_label, label_list=None):
    # initialize count table
    count_table={}
    if(label_list==None):label_list=list(node_to_label.values())
    for row_label in label_list:
        count_table[row_label]={}
        for col_label in label_list:
            count_table[row_label][col_label]=0
    # count
    for node1, node2 in G.edges:
        if((node1 in node_to_label.keys()) and (node2 in node_to_label.keys())): # CAUTION!: Nodes which have no labels will not be considered
            label1=node_to_label[node1]
            label2=node_to_label[node2]
            if(label1==label2):
                count_table[label1][label2]+=1
            else:
                count_table[label1][label2]+=1
                count_table[label2][label1]+=1
    return count_table