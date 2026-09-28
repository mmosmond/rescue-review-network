#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  4 16:12:51 2025

@author: dekens
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as ml
import pandas as pd

ml.rcParams['font.family'] = 'sans-serif'
    


### Import data from csv files
import os

workdir = os.getcwd()
path_network = workdir + '/Network/'

### Load the file summary_composition_commmunities_Q_max.csv
name_file_community_summary = path_network + 'summary_composition_commmunities_Q_max.csv'
data_community_summary = pd.read_csv(name_file_community_summary)

### Sort the data per year
data_community_summary_sorted_per_year =data_community_summary[['Community', 'Title', 'Authors', 'Year']].sort_values(by=['Year'])
### Extract the column indicating the community into a numpy array
list_community_number = data_community_summary_sorted_per_year['Community'].to_numpy()
n_data = len(list_community_number)
n_community = max(list_community_number)

###Extract the column indicating the years into a numpy array
list_year_rough =  data_community_summary_sorted_per_year['Year'].to_numpy()
# delete repetitions of the same year
list_year_sorted = np.unique([int(x) for x in list_year_rough])
min_year, max_year = list_year_sorted[0], list_year_sorted[-1]
## all the years between min and max years
list_year_complete = list(range(min_year, max_year+1))
n_year = len(list_year_complete)

#### Loop to count the number of paper per year
count_per_year_per_community = np.zeros((n_year, n_community))

current_count =0
for year in list_year_rough:
    current_year_entry = int(year - min_year)
    current_community_entry = int(list_community_number[current_count])-1
    count_per_year_per_community[current_year_entry, current_community_entry] =count_per_year_per_community[current_year_entry, current_community_entry] + 1
    current_count = current_count + 1
## Compute the cumulative number of papers per year
cumulative_count_per_year_per_community = np.cumsum(count_per_year_per_community, axis = 0)



### Plot the cumulative number of papers per year
fig, ax = plt.subplots()
#### Getting the same colors for the communities here than for the network
list_community_sorted, len_community_sorted = np.unique([int(x) for x in list_community_number], return_counts=True)  ### community number and size
cum_len_community_sorted = np.append(np.cumsum(len_community_sorted)[::-1], 0)[::-1] ## cumulative community size, need to start at 0
viridis = plt.get_cmap('viridis')
community_colors = viridis(cum_len_community_sorted/(n_data + 2)) ## colors on hte viridis scale in proportion to the community size

### The communities are displayed as colored stacked bars per year
current_bottom = np.zeros(n_year-1)
for j in range(n_community):
    if (len_community_sorted[j]>2):
        plt.bar(list_year_complete[1:], cumulative_count_per_year_per_community[1:, j], bottom =  current_bottom, color = community_colors[j])
    else:
        plt.bar(list_year_complete[1:], cumulative_count_per_year_per_community[1:, j], bottom =  current_bottom, color = 'grey')
    current_bottom = current_bottom + cumulative_count_per_year_per_community[1:, j]

ax.set_xticks(np.arange(1975, 2030, step = 5))
plt.xlim((1974, 2026))
plt.xticks(rotation=90, fontsize = 25) 
plt.yticks(fontsize = 25) 
fig = ax.get_figure()

fig.set_figheight(10)
fig.set_figwidth(20)

plt.ylabel('Cumulative number of publications', fontsize = 40)
plt.xlabel('Year', fontsize = 40)

fig.savefig(path_network+"cumulative_number_of_publications_per_year_per_community.png", bbox_inches='tight')
plt.close()
