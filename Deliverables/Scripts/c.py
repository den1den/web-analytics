import time
from settings import nodes_header, out_nodes_filename, weight_commcenter, weight_normal, \
    classes, edges_header, out_edges_filename, all_years, starting_id_extra, persistent_year, \
    starting_id_persisten_nodes, starting_id_non_persitent_nodes, array_to_gephi_timestamps, \
    values_to_gephi_timstamp_values
from read import read_global_mapping, read_clasification_mapping, read_coauther, write, string_to_pair, \
    get_all_gids_from


start_time = time.time()


# id_map[year][id] = g_id
# years_map[g_id] = [year, ...]
id_map, years_map = read_global_mapping()


classification_mapping, year_purity = read_clasification_mapping(id_map)


pairs = read_coauther(id_map)


def node_output(offset, gid, years):
    timestamp = array_to_gephi_timestamps(years)
    node_class = values_to_gephi_timstamp_values(years, [classification_mapping[y][gid] for y in years])
    return (offset + gid, timestamp, node_class)

#
# Output the nodes
#
# Make the nodes of the year `persistent_year` persistent. So they are only created once for all the years.
# The other nodes 'come and go' and are added for each year
#
output = list()
gids_from_persistent_year = get_all_gids_from(years_map, persistent_year)
for gid in gids_from_persistent_year:
    # These nodes need a combined timestamp
    node_years = years_map[gid]
    output.append(node_output(starting_id_persisten_nodes, gid, node_years))


def is_persistent(gid):
    return gid in gids_from_persistent_year


for gid, years in years_map.items():
    if is_persistent(gid):
        # already added
        pass
    else:
        id =  starting_id_non_persitent_nodes + gid
        for year in years:
            # add a node for each year it is in
            node_years = [year, ]
            output.append(node_output(starting_id_non_persitent_nodes, gid, node_years))
#
# And also add an extra node for each comminuty (only for the presintent nodes)
#
for comm in classes:
    id = starting_id_extra + comm
    timestamp = array_to_gephi_timestamps(all_years)
    clazz = values_to_gephi_timstamp_values(all_years, [comm for y in all_years])
    output.append((id, timestamp, clazz, ))
write(output, nodes_header, out_nodes_filename)


def get_node_id(gid):
    if is_persistent(gid):
        return starting_id_persisten_nodes + gid
    else:
        return starting_id_non_persitent_nodes + gid


#
# Output the edges (just an edge for each node-pair for each year
#
output = list()
weight = weight_normal
edge_id = 1
for pair_str, years in pairs.items():
    a, b = string_to_pair(pair_str)
    src = get_node_id(int(a))
    dst = get_node_id(int(b))
    for y in years:
        timestamp = array_to_gephi_timestamps([y, ])
        output.append((src, dst, "Directed", edge_id, timestamp, weight))
        edge_id += 1
assert edge_id < starting_id_extra
#
# Also output extra (almost weightless) edges between the persistent nodes and the communities
#
weight = weight_commcenter
edge_id = 1
for global_id, years in years_map.items():
    if global_id in gids_from_persistent_year:
        dst = starting_id_persisten_nodes + global_id
        for y in years:
            comm = classification_mapping[y][global_id]
            src = starting_id_extra + comm  # from the hidden comunity node
            id = starting_id_extra + edge_id
            timestamp = array_to_gephi_timestamps([y, ])
            output.append((src, dst, "Directed", id, timestamp, weight))
            edge_id += 1
write(output, edges_header, out_edges_filename)
print("completed in %.3f seconds" % (time.time() - start_time))
