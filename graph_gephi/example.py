'''
Created on 22 Jul 2015

@author: vdthoang
'''
import networkx as nx

G=nx.Graph()
G.add_node('thong', type_='service', node_color='y')
G.add_node(1,type_='number', node_color='r')
G.add_node(2, type_='number', node_color='r')
G.add_node(3,type_='number', node_color='r')
G.add_node(4,type_='number', node_color='r')
G.add_edges_from([(1,2),(1,3),(1,4),(3,4)])
G.add_edges_from([(2, 4, {'color':'blue'})])
G.add_edge(1, 2, weight=4.7)
G.add_edge(1, 'thong', weight=3)
 
print (G.nodes())
 
G.nodes(data=True)
 
print (G.nodes())
 
nx.write_graphml(G,'d:/so.graphml')