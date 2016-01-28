import itertools

all_years = [y for y in range(2001, 2011)]  # 2001, ..., 2010

persistent_year = 2010

classification_input = [
    'graph',    # Reads input from the 200X_pred_label_graph
    'text',     # Reads input from the 200X_pred_label_text
    'baseline'  # Reads input from the author_labels/200X_labels only
][2]

weight_normal = 1.0
weight_commcenter = 0.001

out_nodes_filename = "persistent/%s_nodes_%s.csv" % (persistent_year, classification_input)
out_edges_filename = "persistent/%s_edges_%s.csv" % (persistent_year, classification_input)

starting_id_persisten_nodes = 1000000
starting_id_non_persitent_nodes = 2000000
starting_id_extra = 3000000

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
    'prediction_labels': '../%s_pred_label_' + classification_input + '.txt',
    'baseline_labels': '../author_labels/%s_labels.txt',
    'coauthor': '../adjacent/%s_graph.adjlist',
}

classes = [0, 1, 2, 3, 4, 5]

print_purity = True

recalc_cluster_mapping = False
if recalc_cluster_mapping:
    purity_classification_group_mapping = {
        y: itertools.permutations(classes, 6) for y in all_years
    }
else:
    if classification_input == "graph":
        purity_classification_group_mapping = {
            2001: [(3, 5, 4, 1, 0, 2)],
            2002: [(0, 3, 2, 4, 1, 5)],
            2003: [(1, 3, 0, 2, 5, 4)],
            2004: [(0, 3, 1, 4, 5, 2)],
            2005: [(2, 0, 3, 4, 5, 1)],
            2006: [(3, 0, 5, 2, 4, 1)],
            2007: [(5, 1, 4, 3, 0, 2)],
            2008: [(5, 3, 1, 2, 4, 0)],
            2009: [(3, 5, 2, 0, 1, 4)],
        }
    elif classification_input == "text":
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
    elif classification_input == 'baseline':
        purity_classification_group_mapping = {y: [classes, ] for y in all_years}

assert persistent_year in all_years


def array_to_gephi_timestamps(array):
    floats = [str(float(y)) for y in array]
    return '<[' + ', '.join(floats) + ']>'


def values_to_gephi_timstamp_values(years, values):
    return '"<[' + ']; ['.join([str(float(years[i])) + ', ' + str(values[i]) for i in range(0,len(years))]) + ']>"'
