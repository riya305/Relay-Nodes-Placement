"""
Created on Sat   20 12:20:08 2019

@author: Riya Saxena
"""

import networkx as nx
import matplotlib.pyplot as plt
import random
import sys 
import math
from math import ceil


def distance(sensor_coordinates, i, j):
    dx = sensor_coordinates[i][0] - sensor_coordinates[j][0]
    dy = sensor_coordinates[i][1] - sensor_coordinates[j][1]
    return math.sqrt(dx*dx + dy*dy)

def printMST(G, parent): 
	print("################## Updated Weights ######################")
	for v in range(1,len(G.nodes)): 
		print(parent[v],"-",v,"\t",G[v][ parent[v]]['weight']) 

def findMinNode(key, mstSet, G): 

	min_val= sys.maxsize 
	min_index=-1

	for v in range(len(G.nodes)): 
		if key[v] < min_val and mstSet[v] == False: 
			min_val = key[v] 
			min_index = v 

	return min_index 

def primMST(G): 

	no_of_nodes=len(G.nodes)
	key = [sys.maxsize] * no_of_nodes
	parent = [None] * no_of_nodes 
	key[0] = 0
	mstSet = [False] * no_of_nodes 

	parent[0] = -1

	for cout in range(no_of_nodes): 

		u = findMinNode(key, mstSet, G) 
		mstSet[u] = True
		
		for v in G.neighbors(u): 
			if G[u][v]['weight'] >= 0 and mstSet[v] == False and key[v] > G[u][v]['weight']: 
				key[v] = G[u][v]['weight'] 
				parent[v] = u 

	printMST(G,parent) 
	mst = nx.Graph()
	for v in range(1,len(G.nodes)): 
		mst.add_edge(parent[v],v,weight=G[v][parent[v]]['weight'])
		# print(parent[v],"-",v,"\t",G[v][ parent[v]]['weight']) 
	return mst

def find_min_connected_components(new_mst,budget,communication_range):

	### Assigning weights #########
	sum_weights=0
	for (u,v) in new_mst.edges():
		new_mst.edges[u,v]['weight'] = ceil((new_mst.edges[u,v]['weight']/communication_range))-1
		sum_weights+=new_mst.edges[u,v]['weight']
		print("mst weight")
		print(new_mst.edges[u,v]['weight'])

	while(sum_weights > budget):
		print("Weights")
		print(sum_weights)
		max_edge=max(dict(new_mst.edges).items(), key=lambda x: x[1]['weight'])
		print("Heyyy removing here", max_edge)
		new_mst.remove_edge(*max_edge[0])
		sum_weights=0
		for (u,v) in new_mst.edges():
			sum_weights+=new_mst.edges[u,v]['weight']

	return new_mst
	


def main():

	
	num_sensor_nodes = int(sys.argv[1])
	budget = int(sys.argv[2]) # no of relay nodes
	communication_range= int(sys.argv[3])

	V = []
	V=range(num_sensor_nodes)

	random.seed()

	pos = {i:(random.randint(0,500),random.randint(0,500)) for i in V}

	sensor_coordinates = []
	for i in pos:
	    sensor_coordinates.append(pos[i])

	print("############### Original Weights #########################")
	G=nx.gnm_random_graph(num_sensor_nodes,num_sensor_nodes)

	for (u,v) in G.edges():
		G.edges[u,v]['weight'] = distance(sensor_coordinates, u, v)
		G.edges[v,u]['weight'] = distance(sensor_coordinates, u, v)
		print(u,"-",v,"\t",G.edges[u,v]['weight']) 

	print("##################Networkx Weights#######################")

	T=nx.minimum_spanning_tree(G,algorithm='prim')
	print(sorted(T.edges(data=True)))

	new_mst=primMST(G)
	brand_new_mst=find_min_connected_components(new_mst,budget,communication_range)
	print(sorted(brand_new_mst.edges(data=True)))
	# nx.draw(brand_new_mst)
	
	labels = nx.get_edge_attributes(brand_new_mst,'weight')
	nx.draw_networkx_edge_labels(brand_new_mst,nx.spring_layout(brand_new_mst),edge_labels=labels)
	nx.draw(brand_new_mst)
	plt.show()

if __name__ == "__main__":
    main()
	