#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  4 16:12:51 2025

@author: dekens
"""
import re
import numpy as np
import pandas as pd
import os

workdir = os.getcwd()
path_matrix = workdir+'/Matrix citations/'
path_wos=workdir+'/WOS files/'

#### 1. build dictionnary with wos identification number + title + DOI from csv file

WOS_csv_file = path_wos+"WOS_full_reports_from_request_WOS_titles_20260127.csv"
WOS_df = pd.read_csv(WOS_csv_file)
WOS_title_DOI =WOS_df[['Article Title', 'Authors', 'Publication Year', 'DOI', 'WOS ID']].sort_values(by=['WOS ID']) #### Sort the dictionnary according to the WOS ID column


### 2. build Cited reference list for all paper from WOS full report file .bib
WOS_bib_file = open(path_wos+'WOS_full_reports_from_request_WOS_titles_20260127.bib', 'r').read()

### Build sorted list of WOS ID and list of cited references (with same order)
motif_WOS = '{ WOS'
start_WOS = [m.start() + 2 for m in re.finditer(motif_WOS, WOS_bib_file)] #### Find all occurences of motif_WOS in WOS_bib_file and store as list in start_WOS
# To be able to compare with the previous dictionary, sort the list_WOS_ID, and store the sorting indexes in list_index
list_WOS_ID, list_index = np.unique([WOS_bib_file[x : (x + WOS_bib_file[x:].find(','))] for x in start_WOS], return_index=True) ### Extract the string between each element of start_WOS and the first following occurence of a coma
list_WOS_ID = list(list_WOS_ID) ## convert to list, as np.unique used in previous line returns an array
# reorder start_WOS according to the way list_WOS_ID is sorted
start_WOS_sorted = [start_WOS[list_index[x]] for x in range(len(list_index))]

## Extract the CR for each paper in the order of the WOS ID (through start_WOS_sorted)
motif_CR = "Cited-References = {"
start_CR_after_WOS = [WOS_bib_file[x:].find(motif_CR) + x + len(motif_CR) for x in start_WOS_sorted] ### Search for the first occurences of motif_CR after motif_WOS
list_CR = [WOS_bib_file[x : (x + WOS_bib_file[x:].find('},\n'))] +'\n' for x in start_CR_after_WOS] ####the additional \n added at the end of the list is a technical adding to alloz to filter the last DOI the same as others (see below)

## Build a list (for each CR) of the list of cited DOIs in the CR
motif_DOI_CR = 'DOI '
start_DOI_CR =  [[m.start() + len(motif_DOI_CR) for m in re.finditer(motif_DOI_CR, CR)] for CR in list_CR]
list_DOIs_list_CR = [[CR[x: (x + min(end for end in [CR[x:].find('.\n'), CR[x:].find(',')] if end > 0))] for x in start_DOI] for (start_DOI, CR) in zip(start_DOI_CR, list_CR)]  # list of lists of DOIs in Cited references for each paper
## the additional find ',' is because some cited references have multiple DOIs


## 3. Finally construct the matrix of citations using list_DOI (in the order of WOS ID) and the list_DOIs_list_CR
list_DOI = list(WOS_title_DOI['DOI'])
list_WOS_ID_from_csv = list(WOS_title_DOI['WOS ID'])

matrix_citations = np.zeros((len(list_DOI), len(list_DOI)))
for k in range(len(list_DOI)):
    current_DOI = list_DOI[k]
    current_CR_DOis = list_DOIs_list_CR[k]
    for l in range(len(list_DOI)):
        matrix_citations[k, l] = current_CR_DOis.count(list_DOI[l])
####matrix_citations[k, l] = how many times DOI l appears in cited reference of k (ie; how many times k cites l)

    
## 4. Save the matrix_citations as csv file using pandas and list of titles as headers

path_matrix = workdir+'/Matrix citations/'
list_titles = list(WOS_title_DOI['Article Title'])

        
df_matrix_citations_titles = pd.DataFrame(matrix_citations, index = list_titles, columns = list_titles)
df_matrix_citations_titles.to_csv(path_matrix+'matrix_citations_titles.csv')


## Save the matrix_citations as csv file using pandas and list of authors as headers
list_authors = list(WOS_title_DOI['Authors'])

df_matrix_citations_authors = pd.DataFrame(matrix_citations, index = list_authors, columns = list_authors)
df_matrix_citations_authors.to_csv(path_matrix+'matrix_citations_authors.csv')

## Save the matrix_citations as csv file using pandas and list of Publicationyear
list_pub_year = list(WOS_title_DOI['Publication Year'])

df_matrix_citations_pub_year = pd.DataFrame(matrix_citations, index = list_pub_year, columns = list_pub_year)
df_matrix_citations_pub_year.to_csv(path_matrix+'matrix_citations_pub_year.csv')

