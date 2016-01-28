import time

from settings import *
from read import *

start_time = time.time()

base_year = all_years[0]
comp_years = all_years[1:len(all_years)-1]

out_nodes_filename = "c/compare_to_%s_nodes.csv" % (base_year, )
out_edges_filename = "c/compare_to_%s_edges.csv" % (base_year, )

print("Comparing "+str(base_year)+" to "+str(comp_years) + " see output in c/")

# id_map[year][id] = gid
# years_map[gid] = [year, ...]
id_map, years_map = read_global_mapping()
# year_classification_mapping[y][gid] = comm
classification_mapping, year_purity = read_clasification_mapping(id_map)
# pairs[pair_str] = [year, ...]
pairs = read_coauther(id_map)

#
# Output the nodes in base_year
#
node_header = ['id', 'my_node_type']
output = list()
base_nodes = get_all_gids_from(years_map, base_year)
my_type = 'bc_%s' % base_year
for gid in base_nodes:
    output.append((
        starting_id_persisten_nodes + gid,
        my_type,
    ))
# output the new nodes in each compared year
for gid, years in years_map.items():
    if gid in base_nodes:
        # not new
        pass
    else:
        # this node is new
        for y in years:
            if y in comp_years:
                output.append((
                    starting_id_non_persitent_nodes + gid,
                    'new_'+str(y)
                ))
#
# And also add an extra node for each comminuty (only for the presintent nodes)
#
for comm in classes:
    output.append((
        starting_id_extra + comm,
        'comm_' + str(comm)
    ))
write(output, node_header, out_nodes_filename)


def get_node_id(gid):
    if gid in base_nodes:
        return starting_id_persisten_nodes + gid
    else:
        return starting_id_non_persitent_nodes + gid


#
# Output the edges for the normal year
#
output = list()
weight = weight_normal
edge_id = 1
my_type = "bc_" + str(base_year)
base_edges = list()
for pair_str, years in pairs.items():
    if base_year in years:
        # this edge existed during base_year
        a, b = string_to_pair(pair_str)
        src = get_node_id(int(a))
        dst = get_node_id(int(b))
        output.append((src, dst, "Directed", starting_id_persisten_nodes + edge_id, my_type, weight))
        base_edges.append(pair_str)
        edge_id += 1
assert edge_id < starting_id_persisten_nodes
#
# Also output extra (almost weightless) edges between the communities nodes and the normal year nodes
#
weight = weight_commcenter
edge_id = 1
type_format = "comm_%s"
for gid, comm in classification_mapping[base_year].items():
    my_type = type_format % comm
    dst = starting_id_extra + comm
    src = starting_id_persisten_nodes + gid
    output.append((src, dst, "Directed", starting_id_extra + edge_id, my_type, weight))
    edge_id += 1
#
# Also output edges of the new nodes
#
weight = weight_normal
edge_id = 1
type_format = "new_%s"
for pair_str, years in pairs.items():
    if pair_str not in base_edges:
        a, b = string_to_pair(pair_str)
        gida = int(a)
        gidb = int(b)
        for y in years:
            if y in comp_years:
                src = get_node_id(gida)
                dst = get_node_id(gidb)
                my_type = type_format % y
                output.append((src, dst, "Directed", starting_id_non_persitent_nodes + edge_id, my_type, weight))
                edge_id += 1
write(output, ['Source', 'Target', 'Type', 'id', 'my_edge_type', 'weight'], out_edges_filename)
print("completed in %.3f seconds" % (time.time() - start_time))
