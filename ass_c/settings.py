import itertools

all_years = [y for y in range(2001, 2010)]
gt = "text" # graph or text

weight_normal = 1.0
weight_commcenter = 0.01

out_nodes_filename = "nodes.csv"
out_edges_filename = "edges.csv"

starting_extra_id = 9999990

edges_header = ['Source', 'Target', 'Type', 'id', 'timeset', 'weight']
# Source: source node id
# Target: target node id
# Type: directed/undirected
# id: the is of some node ( > 9999990 means extra edge)
# timeset: array of years this edge is in
# weight: the weight of this edge

nodes_header = ['id', 'timeset', 'commclass']
# id: the global id ( > 9999990 means extra node)
# timeset: array of years this node is in
# commclass: the community that some node is in


filenames = {
    'author_mapping': '../author_mapping/%s_mapping.txt',
    'prediction_labels': '../%s_pred_label_' + gt + '.txt',
    'baseline_labels': '../author_labels/%s_labels.txt',
    'coauthor': '../adjacent/%s_graph.adjlist',
}

classes = [0, 1, 2, 3, 4, 5]

purity_classification_group_mapping_ = {
    y: itertools.permutations(classes, 6) for y in all_years
}

purity_classification_group_mapping = {
    2001: [(1, 2, 0, 4, 5, 3)],
    2002: [(2, 4, 3, 1, 0, 5)],
    2003: [(1, 2, 5, 4, 3, 0)],
    2004: [(4, 3, 0, 2, 5, 1)],
    2005: [(1, 2, 3, 4, 0, 5)],
    2006: [(1, 5, 2, 0, 4, 3)],
    2007: [(4, 3, 0, 5, 2, 1)],
    2008: [(0, 2, 1, 3, 5, 4)],
    2009: [(1, 4, 0, 2, 5, 3)],
}

