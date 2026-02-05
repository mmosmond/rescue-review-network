#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 21 14:22:11 2025

@author: dekens

"""
########### Main code for the modularity maximisation analysis. 
###It uses the auxiliary tools_modular_seeds code file (same directory) and the connectivity matrix data (first two csv files, same directory)
import networkx as nx
import pandas as pd
import tools_network_citation_analysis_evol_rescue as tools
import numpy as np
import os

workdir = os.getcwd()

path_tex=workdir+'/TeX files/'
path_matrix = workdir+'/Matrix citations/'
path_subsection = workdir + '/Subsections/'

path_network = workdir + '/Network/'

Nseed = 1000
Seed = range(Nseed) 


#### Import data from csv files

name_file_titles = path_matrix+"matrix_citations_titles.csv"
name_file_authors = path_matrix+"matrix_citations_authors.csv"
name_file_pub_year = path_matrix+"matrix_citations_pub_year.csv"

data_titles = pd.read_csv(name_file_titles)
data_authors = pd.read_csv(name_file_authors)
data_pub_year = pd.read_csv(name_file_pub_year)

### Convert to numpy array using pandas
mat_titles = pd.DataFrame(data_titles).to_numpy()
mat_authors = pd.DataFrame(data_authors).to_numpy()
mat_pub_year = pd.DataFrame(data_pub_year).to_numpy()

### Dictionary, key: index, values: titles, authors or pub year
nodelist_titles = dict(zip(range(len(mat_titles[:, 0])), list(mat_titles[:, 0])))
nodelist_authors = dict(zip(range(len(mat_authors[:, 0])), list(mat_authors[:, 0])))
nodelist_pub_year = dict(zip(range(len(mat_pub_year[:, 0])), list(mat_pub_year[:, 0])))

##" Adjacency matrix (matrix of the neighboors)
adj_mat = mat_titles[:, 1:].astype(float)
number_of_citations_within = np.sum(adj_mat, axis = 0)

#### Creating the directed graphs from the adjacency matrices using Digraph from NetworkX

G = nx.DiGraph(adj_mat)

############ Run the louvain_comminities function from the community subpackage of the NetworkX package

### Resolution parameter for the louvain algorithm
Resolution = np.linspace(.8, 1.2, num = 21)

count = 0

## dynamically store seed, resolutin and partition for Q_max (maximum of modularity coefficient)
partition_max = []
resolution_max = 0
seed_max = 0
Q_max = 0
for seed in Seed:
    count_res = 0
    for resolution in Resolution:
        #### Find communities and compute modularity associated
        
        ## Louvain method: return a list of communities louvain_communities
        louvain_communities = tools.sorted_partition(nx.community.louvain_communities(G, resolution=Resolution[count_res], threshold=1e-10, seed=seed))
        
        ## Return the modularity coefficient of the list of communties found previously
        Q_louvain = nx.community.modularity(G, louvain_communities)
        if (Q_louvain > Q_max):
            Q_max = Q_louvain
            partition_max = louvain_communities
            seed_max = seed
            resolution_max = resolution
        count_res = count_res + 1
    print(seed)

print("max")
print(seed_max)
print(resolution_max)
print(Q_max)



partition_max = tools.sorted_partition(partition_max)
tools.save_json_gz(partition_max, path_network + '/partition_max')

## Write the composition of the communities in txt and csv files with additional information (author, year of publication, number of citations within network)
tools.write_communities_composition_to_txt_and_csv(partition_max, nodelist_titles, nodelist_authors, nodelist_pub_year, number_of_citations_within, path_network)



#### Before plotting, get the names of the subsections
names_subsection_file = open(path_subsection+ 'names_subsection.txt', 'r')
names_subsection = [x[:-1] for x in list(names_subsection_file)]
names_subsection_file.close()
###Plot
tools.modular_graph_layout_per_subsection_and_all(G, partition_max, 'network_citations_evol_rescue_resolution =%4.2f'%resolution_max, Q= Q_max, nodelist=G.nodes, name_subsection= names_subsection, path_network=path_network, path_subsection=path_subsection)

