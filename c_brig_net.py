from graphspace_python.api.client import GraphSpace
from graphspace_python.graphs.classes.gsgraph import GSGraph
from graphspace_python.graphs.classes.gslayout import GSLayout
import sys
import math
import random
import copy
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def main():
	#file from the affiliated Github repo of Schneider et al. 2021
	el, nl = read_edge_list('./SSN_mc476_edgelist.csv')
	adj_list  = el_to_ajlist(el, nl)

	#calculate network measures
	cc = calculate_closeness(adj_list)
	sp = all_pairs_shortest_paths(adj_list)
	dd = get_degree_dist(adj_list)
	eb = edge_betweenness(adj_list,el)
	andeg = avg_neighbor_degree(adj_list)
	clusc = clustering_coeff(adj_list)

	#make plots
	#plot_degree_dist(dd)
	#plot_closeness_centrality_dist(cc)
	#plot_eb_dist(eb)
	#plot_clus_coef(clusc)
	plot_and(andeg)

	#to GraphSpace
	#make_graph_cc(nl, el, cc,'Transposon Similarity Net with Closeness Centrality1')
	#make_graph_and(nl, el, andeg,'Transposon Similarity Net with Average Neighbor Degree4')
	#make_graph_clusc(nl, el, clusc,'Transposon Similarity Net with Clustering Coeff 4')
	#print(eb)



##################################
##Plot distributions
##################################
def plot_and(andeg):
	#adjust for log
	#ploand = np.log(list(andeg.values()))
	ploand = andeg.values()
	plt.hist(ploand, bins =20)
	plt.xlabel('Average Neihbor Degree')
	plt.ylabel('Frequency')
	plt.savefig('./figures/andeg_bins_20.png')

def plot_degree_dist(dd):
	#adjust for log
	plodd = np.log(list(dd.values()))
	#plodd = dd.values()
	plt.hist(plodd, bins =40)
	plt.xlabel('Node Degree')
	plt.ylabel('Log Frequency')
	plt.savefig('./figures/dd_log_bin_1.png')

def plot_closeness_centrality_dist(cc):
	plocc = cc.values()
	plt.hist(plocc,bins=20)
	plt.xlabel('Closeness Centrality')
	plt.ylabel('Frequency')
	plt.savefig('./figures/cc_bins_20.png')

def plot_eb_dist(eb):
	#ploeb = eb.values()
	ploeb = np.log(list(eb.values()))
	plt.hist(ploeb,bins=15)
	plt.xlabel('Edge Betweeness')
	plt.ylabel('Frequency')
	plt.savefig('./figures/eb_bins_15_log.png')

def plot_clus_coef(clusc):
	ploecl = clusc.values()
	#plocl = np.log(list(clusc.values()))
	plt.hist(ploecl,bins=15)
	plt.xlabel('Clustering Coefficient')
	plt.ylabel('Frequency')
	plt.savefig('./figures/clusc_15.png')

##################################
##Graphs to GraphSpace
##################################

#plot to graphspace with nodes sized and colored by closeness centrality
def make_graph_cc(nl, el, cc, gname):
	maxm = max(cc.values())
	G = GSGraph()
	G.set_tags(['Independent Project'])
	G.set_name('CC Transposon')
	for n in nl:
		G.add_node(n,label=n)
		G.add_node_style(n,color=rgb_to_hex(0.5,1-cc[n]/maxm,cc[n]/maxm),height=cc[n]*8000,width=cc[n]*8000)

	for e in el:
		G.add_edge(e[0],e[1])
		G.add_edge_style(e[0],e[1],width=2)

	graph_name = input(gname)
	G.set_name(gname)
	email = input('Enter Email:')
	password = input('Enter Password:')
	gs = GraphSpace(email,password)
	print('GraphSpace successfully connected.')

	graphy = gs.post_graph(G)


	## Print details about the graph & group
	group='BIO331F21'
	gs.share_graph(graph=graphy,group_name=group)
	print('Graph successfully posted to %s group.' % (group))
	groupid = gs.get_group(group_name=group).id
	return

#plot to graphspace with nodes sized and colored by clustering coefficient
def make_graph_clusc(nl, el, cc, gname):
	maxm = max(cc.values())
	G = GSGraph()
	G.set_tags(['Independent Project'])
	G.set_name('CC Transposon')
	for n in nl:
		G.add_node(n,label=n)
		G.add_node_style(n,color=rgb_to_hex(0.5*cc[n]/maxm,1-cc[n]/maxm,1),height=np.log(cc[n]*1000)*15,width=np.log(cc[n]*1000)*15)

	for e in el:
		G.add_edge(e[0],e[1])
		G.add_edge_style(e[0],e[1],width=2)

	graph_name = input(gname)
	G.set_name(gname)
	email = input('Enter Email:')
	password = input('Enter Password:')
	gs = GraphSpace(email,password)
	print('GraphSpace successfully connected.')

	graphy = gs.post_graph(G)


	## Print details about the graph & group
	group='BIO331F21'
	gs.share_graph(graph=graphy,group_name=group)
	print('Graph successfully posted to %s group.' % (group))
	groupid = gs.get_group(group_name=group).id
	return

def make_graph_and(nl, el, cc, gname):
	maxm = max(cc.values())
	G = GSGraph()
	G.set_tags(['Independent Project'])
	G.set_name('CC Transposon')
	for n in nl:
		G.add_node(n,label=n)
		G.add_node_style(n,color=rgb_to_hex(0,cc[n]/maxm,1-cc[n]/maxm),height=cc[n]*4,width=cc[n]*4)

	for e in el:
		G.add_edge(e[0],e[1])
		G.add_edge_style(e[0],e[1],width=2)

	graph_name = input(gname)
	G.set_name(gname)
	email = input('Enter Email:')
	password = input('Enter Password:')
	gs = GraphSpace(email,password)
	print('GraphSpace successfully connected.')

	graphy = gs.post_graph(G)


	## Print details about the graph & group
	group='BIO331F21'
	gs.share_graph(graph=graphy,group_name=group)
	print('Graph successfully posted to %s group.' % (group))
	groupid = gs.get_group(group_name=group).id
	return

## RGB to Hex function - copied from Lab 3
def rgb_to_hex(red,green,blue): # pass in three values between 0 and 1
  maxHexValue= 255  ## max two-digit hex value (0-indexed)
  r = int(red*maxHexValue)    ## rescale red
  g = int(green*maxHexValue)  ## rescale green
  b = int(blue*maxHexValue)   ## rescale blue
  RR = format(r,'02x') ## two-digit hex representation
  GG = format(g,'02x') ## two-digit hex representation
  BB = format(b,'02x') ## two-digit hex representation
  return '#'+RR+GG+BB


##################################
##Network creation, manipulation, and metric calculation
##################################


#From my HW2.py
#read in edge list. Final format is a dictionary with 
#keys as edges and edge weights as values. 
def read_edge_list(file):
	el = {}
	nl = []
	with open(file) as fin:
		for line in fin:
			edge1, edge2, weight = line.strip().split()
			edge1 = edge1[23:]
			edge2 = edge2[23:]
			el[(edge1,edge2)] = weight
			if edge1 not in nl:
				nl.append(edge1)
			if edge2 not in nl:
				nl.append(edge2)
	return el, nl

#convert edge list (works with my edge-weight format added, as seen above) 
#to an adjacency list.
def el_to_ajlist(edge_list, node_list):
	#following four lines of code from Anna ritz's 'lab3_utils.py' fom lab3
	adj_list = {n:[] for n in node_list}  
	for e in edge_list:
		adj_list[e[0]].append(e[1])
		adj_list[e[1]].append(e[0])
	return adj_list

def calculate_closeness(adj_list):
    #returns a dictionary of closeness centralities with nodes as keys and closeness centrality as values
    cc = {}
    for v in adj_list.keys():
        #for each node in adj_list, return the reciprocal of the sum of the lengths of the shortest paths
        #of every other node to the given node.
        cc[v] = 1/sum(x for x in shortest_paths_hw2(adj_list,v).values())
    return cc

def clustering_coeff(adjlisty):
	cccs = {}

	emax = len(adjlisty.keys())
	for key in adjlisty.keys():
		cccs[key] = len(adjlisty[key])/emax
	return cccs

#From my Lab2.py submission
def avg_neighbor_degree(adjlist) -> dict:
	andeg = {}
	for key in adjlist.keys():
		count = 0
		for subkey in adjlist[key]:
			count+=len(adjlist[subkey])
		andeg[key] = count/len(adjlist[key])
	return andeg

def get_degree_dist(adj_list):
	#returns a dictionary of degree distributions with nodes as keys and closeness centrality as values
	dd = {}
	#degree 
	for node in adj_list.keys():
		dd[node] = len(adj_list[node])

	return dd

#from my HW2.py
def shortest_paths_hw2(G,s):
    #input G (an adj_list) and a given node, then return a dictionary of all nodes as
    #keys and the length of each shortest path between nodes (an int) as entries.
    D = {}
    for n in G.keys():
        D[n] = float('inf') 
    D[s] = 0
    #define D as the shortest paths dictionary, instantiate all nodes as keys in D with values as infinity floats
    #then define the given node 's' as 0, since the shortest path between a node and itself is 0

    Q = [s]
    #makes a queue list of nodes

    #while there are entries in the queue list, remove the first node in the list, then for all neighbors of the
    #given node check if the neighbors have't been visited before (their values wil be infinity,) and they have
    #not, then input the neighbor's shortest paths value. 
    while Q != []:
        w = Q.pop(0)
        for x in G[w]:
            if D[x] == float('inf'):
                D[x] = D[w] + 1
                Q.append(x)

    return D

#From Anna Ritz's HW3_utils.py
def shortest_paths_hw3(adj_list, n):
    # initialize distances dictionary & predecessors dictionary
    dist = {n:float('inf') for n in adj_list.keys()}
    predecessors = {n:[] for n in adj_list.keys()}
    dist[n] = 0
    predecessors[n] = None

    # initialize to_explore list
    to_explore = [n]

    while len(to_explore) > 0: # while there's still a node to explore...
        exploring = to_explore.pop(0) # remove the FIRST node from to_explore

        # for every neighbor, check if it has been visited
        for neighbor in adj_list[exploring]:
            if dist[neighbor] == float('inf'): # unexplored
                # update the distance to neighbor
                dist[neighbor] = dist[exploring] + 1
                # update where we came from.
                predecessors[neighbor].append(exploring)
                # add neighbor to the to_explore list
                to_explore.append(neighbor)
            # catch ties and add predecessors
            elif dist[neighbor] == dist[exploring]+1:
                predecessors[neighbor].append(exploring)
    return dist,predecessors

#From Anna Ritz's HW3_utils.py
def all_pairs_shortest_paths(adj_list):
    paths = {}
    for u in list(adj_list.keys()): # for every node...
        paths[u] = {}
        # get shortest paths & node predecessors from this node
        dist,predecessors = shortest_paths_hw3(adj_list,u)

        # get the paths for nodes with a non-inf or non-zero distance.
        for v in dist:
            if u == v or dist[v]==float('inf'):
                paths[u][v] = []
            else:
                paths[u][v] = get_paths(predecessors,v,[[v]])
    return paths

#from hw3_utils.py
def get_paths(predecessors,n,curr_paths):
    # base case
    # we've reached the first node; we're done.
    if predecessors[n] == None:
        return curr_paths

    # there's still at least one node to backtrack.
    # for each predecessor, prepend the predecessor and call
    # get_paths() for the predecessor.
    new_paths = []
    for pred in predecessors[n]:
        these_paths = []
        for i in range(len(curr_paths)):
            these_paths.append([pred]+curr_paths[i])
        new_paths+=get_paths(predecessors,pred,these_paths)
    return new_paths

#from my HW3
def edge_betweenness(adj_list,edge_list):
    #calculate shortest paths
    paths = all_pairs_shortest_paths(adj_list)
    edge_betweeny = {}
    #put edges in the edge_betweeny dictionary and make their values be 0
    for edge in edge_list:
        edge_betweeny[edge] = 0
    
    #uses the shortest paths function in the utilities file.
    #The length of each shortest path is halved, as it will be counted twice for
    #the final edge betweeness
    for nod1 in paths.keys():
        for nod2 in paths[nod1].keys():
            if len(paths[nod1][nod2]) >0:
                for lis in paths[nod1][nod2]:
                    if len(lis)>0:
                        for x in range(len(lis)-1):
                            try:
                                edge_betweeny[lis[x],lis[x+1]]+=0.5/len(paths[nod1][nod2])
                            except:
                                edge_betweeny[lis[x+1],lis[x]]+=0.5/len(paths[nod1][nod2])

    return edge_betweeny


if __name__ == '__main__':
	main()
