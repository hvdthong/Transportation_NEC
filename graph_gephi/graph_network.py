__author__ = 'vdthoang'
from main.loadFile import load_file
import networkx as nx
def graph_constructed(path, name):
    list_line = load_file(path, name)

    list_source_nodes = []
    list_target_nodes = []

    DG = nx.DiGraph()
    for line in list_line:
        split_line = line.strip().split('\t')
        target = split_line[0]
        source = split_line[1]
        type = split_line[2]
        weight = int(split_line[3])

        if (source not in list_source_nodes):
            list_source_nodes.append(source)
            DG.add_node(source, type_ = type)

        if (target not in list_target_nodes):
            list_target_nodes.append(target)
            DG.add_node(source, type_ = 'target')

        DG.add_weighted_edges_from([(source, target, weight)])

    DG.nodes(data=True)
    nx.write_graphml(DG,'d:/' + name.replace('.csv', '') + '.graphml')

if __name__ == '__main__':
    path = 'd:/'
    name = 'allschemas_busservices.csv'
    graph_constructed(path, name)