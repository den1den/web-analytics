import time
start_time = time.time()
from settings import nodes_header, out_nodes_filename, weight_commcenter, weight_normal, \
    classes, edges_header, out_edges_filename, all_years, starting_id_extra, persistent_year, \
    starting_id_persisten_nodes, starting_id_non_persitent_nodes, array_to_gephi_timestamps, \
    values_to_gephi_timstamp_values
from read import read_global_mapping, read_clasification_mapping, read_coauther, write, string_to_pair, \
    get_all_gids_from

base_year = all_years[0]
comp_years = all_years[1:len(all_years)-1]

out_nodes_filename = "3/compare_to_%s_nodes.csv" % (base_year, )
out_edges_filename = "3/compare_to_%s_edges.csv" % (base_year, )

print("Comparing "+str(base_year)+" to "+str(comp_years) + " see output in 3/")

# id_map[year][id] = g_id
# years_map[g_id] = [year, ...]
id_map, years_map = read_global_mapping()


classification_mapping, year_purity = read_clasification_mapping(id_map)

# pairs[pair_str] = [year, ...]
pairs = read_coauther(id_map)

#
# Output the nodes in base_year
#
node_header = ['id', 'my_type']
output = list()
base_nodes = get_all_gids_from(years_map, base_year)
for gid in base_nodes:
    output.append((
        starting_id_persisten_nodes + gid,
        'bc'+str(base_year),
    ))
# output the nodes in the compared year
for y in comp_years:
    id_map_y = id_map[y]
    for bak, g_id in id_map_y.items():
        if g_id in base_nodes:
            # this node is also in the compared year relation
            pass
        else:
            # this node is new
            output.append((
                starting_id_non_persitent_nodes + g_id,
                'new'+str(base_year)
            ))
#
# And also add an extra node for each comminuty (only for the presintent nodes)
#
for comm in classes:
    output.append((
        starting_id_extra + comm,
        'comm' + str(comm)
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
type = "bc" + str(base_year)
for pair_str, years in pairs.items():
    if base_year in years:
        # this edge existed during base_year
        a, b = string_to_pair(pair_str)
        src = get_node_id(int(a))
        dst = get_node_id(int(b))
        output.append((src, dst, "Directed", starting_id_persisten_nodes + edge_id, type, weight))
        edge_id += 1
assert edge_id < starting_id_persisten_nodes
#
# Also output extra (almost weightless) edges between the communities nodes and the normal year nodes
#
weight = weight_commcenter
edge_id = 1
type_format = "bccomm%s"
for comm in classes:
    type = type_format % comm
    dst = starting_id_extra + comm
    for g_id in classification_mapping[base_year]:
        src = starting_id_persisten_nodes + g_id
        output.append((src, dst, "Directed", starting_id_extra + edge_id, type, weight))
        edge_id += 1
#
# Also output edges of the new nodes
#
weight = weight_normal
edge_id = 1
type_format = "new%s"
for pair_str, years in pairs.items():
    a, b = string_to_pair(pair_str)
    gida = int(a)
    gidb = int(b)
    # check if this edge contains a new node for each new year
    for y in years:
        if y != base_year:
            # the edge existed in some year different then base year
            if not (gida in base_nodes) or not (gidb in base_nodes):
                # this edge is connected to a new node
                src = get_node_id(gida)
                dst = get_node_id(gidb)
                type = type_format % y
                output.append((src, dst, "Directed", starting_id_non_persitent_nodes + edge_id, type, weight))
                edge_id += 1

write(output, ['Source', 'Target', 'Type', 'id', 'my_type', 'weight'], out_edges_filename)
print("completed in %.3f seconds" % (time.time() - start_time))
