### Auxiliary code file with functions used in the main file (to place in the same directory)
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as ml
import pandas as pd
ml.rcParams['mathtext.fontset'] = 'stix'
ml.rcParams['font.family'] = 'sans-serif'
plt.rcParams.update({
    "text.usetex": True})


####### Create a directory of path workdir
def create_directory(workdir):
    import os
    try:
        os.mkdir(workdir)
        print("Directory " , workdir ,  " Created ") 
    except FileExistsError:
        print("Directory " , workdir ,  " already exists")
    return

def write_communities_composition_to_txt_and_csv(partition, titles, authors, pub_year, citations, path_network):
    #### Write the composition of each communities
    txt_file = open(path_network +  'composition_commmunities_Q_max.txt', 'w')
    df = pd.DataFrame([], index = [], columns =['Community', 'Title', 'Authors', 'Year'])
    count = 1 
    for c in partition:
        txt_file.write("-------------------COMMUNITY %i"%count +'----------------------\n')
        for x in c:
            txt_file.write('   %i'%x +': '+titles[x] +', ' + authors[x]+', %i'%pub_year[x]+', number of citations within network = %i'%citations[x]+'\n\n')
        #print(len(c))
        txt_file.write('\n\n')
        community_data = zip([count for x in c], [titles[x] for x in c], [authors[x] for x in c], [pub_year[x] for x in c])
        community_df = pd.DataFrame(community_data, index = ([x for x in c]), columns =['Community', 'Title', 'Authors', 'Year'])
        df = pd.concat([df, community_df])
        count = count + 1
    txt_file.close()
    df.to_csv(path_network +'summary_composition_commmunities_Q_max.csv')
    return()

### Function to sort the list of communities (partition) according to the first element of each community itself sorted in increasing order of neuron
def sorted_partition(partition):
    partition_sorted_1 = [sorted(c) for c in partition] ## sort within communities
    partition_sorted_2 = sorted(partition_sorted_1, key=len, reverse=True) ## sort between communities
    return(partition_sorted_2)


#### Same function, but with transparency for each node and edge according to the transparency. Possibility for different type of commmunity layout
def modular_graph_layout_per_subsection_and_all(G, partition, name, Q, nodelist, name_subsection, path_network, path_subsection):
    large_communities = [x for x in partition if (len(x) > 2)]
    small_communities = [x for x in partition if (len(x) <= 2)]
    n_small_communities = len(small_communities)
    ### Positions of the communities: set for large communities and random for small ones
    offsets_large_communities =[ [0, 0],  [-3, -24], [19,-5], [17, 18], [-1, 20], [-18,15], [-19, - 1], [-17, - 19]]
    import random as rd
    offsets_small_communities = [[18+ rd.uniform(-5, 5), -25 + rd.uniform(-5, 5)]  for k in range(n_small_communities)]
    
    ### Defining the positions of the nodes of large communities, loop on communities
    pos = {}
    for offset, nodes in zip(offsets_large_communities, large_communities):
        Gsubgraph = G.subgraph(nodes)
        ### Choose appropriate k and scale parameters for nx.spring_layout depending on the size of the community
        if (len(nodes)<5):
            k = 0.1
            scale = 1
        else:
            if (len(nodes)<10):
                k = 1.3
                scale = len(nodes) // 3
            else:
                if (len(nodes)<40):
                    k = 1.3
                    scale = len(nodes) // 5  
                else:
                    k = 1.4
                    scale = len(nodes) // 4.05
        community_position = nx.spring_layout(Gsubgraph, center=offset, k = k, scale = scale)
        pos = {**pos, **community_position}
    ### Defining the positions of the nodes of small communities, loop on communities        
    for offset, nodes in zip(offsets_small_communities, small_communities):
        Gsubgraph = G.subgraph(nodes)
        k = 0.2
        scale = 0.5
        community_position = nx.spring_layout(Gsubgraph, center=offset, k = k, scale = scale)
        pos = {**pos, **community_position}
   
    ### Coloring nodes in function of their communities
    viridis = ml.colormaps['viridis']
    binary = ml.colormaps['binary']
    node_color= np.empty((len(G.nodes), 4))
    prop_len_community = 0 ### normalised size of communities
    for c in partition:
        if (len(c)>2):
            node_color[list(c)] = viridis(np.ones(len(c))*prop_len_community)
            prop_len_community= prop_len_community + len(c)/(len(G.nodes) + 2)
            print(prop_len_community)
        else:
            node_color[list(c)] = binary(np.ones(len(c))*1/2)

    ### Draw the full graph
    fig, ax = plt.subplots(1, 1, figsize = (50, 50))
    edge_width = [w*2 for (*edge, w) in G.edges.data('weight')]
    node_size = 5000
    nx.draw_networkx(G, pos=pos, node_color = node_color, width = edge_width, arrows = True, labels = nodelist, font_size = 16, connectionstyle='arc3, rad=.15', alpha = 0.5, node_size = node_size*np.array([G.degree(node)**(1/2.5) for node in G.nodes]))
    nx.draw_networkx_labels(G, pos=pos, font_size = 40, alpha= 0.8)
    plt.title('Q = %4.5f'%Q, fontsize = 80)
    plt.savefig(path_network + name + '.png', dpi = 100)
    #plt.show()
    plt.close()
    
    ### Additional plots for each subsection, using transparency to highlights the nodes in the subsection
    Nsubsection = len(name_subsection)
    for i in range(Nsubsection-1):
        filter_subsection = list(pd.read_csv(path_subsection +'filter_subsection %i'%i +'.csv')['0'])
        transparency =  [min(x + 0.1, .5) for x in filter_subsection]
        ### Draw the graph by drawing nodes, labels and edges with transparency
        fig, ax = plt.subplots(1, 1, figsize = (40, 40))
        edge_width = [w*2 for (*edge, w) in G.edges.data('weight')]
        node_size = 5000
        
        edge_transparency = [transparency[node1]*transparency[node2] for (node1, node2) in G.edges]
        nx.draw_networkx_nodes(G, pos=pos, nodelist=nodelist, node_color = node_color, node_size = node_size*np.array([G.degree(node)**(1/2.5) for node in G.nodes]), alpha =transparency)
        nx.draw_networkx_labels(G, pos=pos, font_size = 40, alpha= dict(zip(G.nodes, [x for x in transparency])))
        node_size = 25000
        nx.draw_networkx_edges(G, pos=pos, edgelist=G.edges, alpha = edge_transparency, width = edge_width, nodelist = G.nodes, node_size = node_size, arrows = True, connectionstyle='arc3, rad=.15')       
        plt.title(name_subsection[i], fontsize = 100)
        plt.savefig(path_network + name +'_' +name_subsection[i] + '.png')
        #plt.show()
        plt.close()
    return()




### Miscellaneous practical functions

def convert_list_of_sets_into_list_of_lists(l):
    return([list(x) for x in l])

def write_nodelist(nodelist, name):
    f = open(name + '.txt', 'a')
    f.write("{\n")
    for k in nodelist.keys():  
        print(k)      
        f.write(F"'{k}': '{nodelist[k]}',\n")  # add comma at end of line
    f.write("}")
    f.close()
    return()

def w_communities(communities, Q, nodelist, name):
    f = open(name + '.txt', 'a')
    f.write("Modularity score is Q="+F"'{Q}'.\n")
    idx_c = 1
    for c in communities:
        f.write("Community " +F"'{idx_c}': '{[nodelist[i] for i in c]}'.\n")
        idx_c += 1
    f.close()
    return()

def save_json_gz(obj, filepath):
    import gzip
    import json

    json_str = json.dumps(obj)
    json_bytes = json_str.encode()
    with gzip.GzipFile(filepath, mode="w") as f:
        f.write(json_bytes)
        
def load_json_gz(filepath):
    import gzip
    import json

    with gzip.open(filepath, 'r') as fin:       
        json_bytes = fin.read()                   

    json_str = json_bytes.decode()           
    data = json.loads(json_str)
    return(data)


    
def write_csv_from_zip(data_zip, path):
    import csv

    with open(path, "w") as f:
        writer = csv.writer(f)
        for row in data_zip:
            writer.writerow(row)
    return()

