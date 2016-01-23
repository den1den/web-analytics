import time
from settings import nodes_header, nodes_format, out_nodes_filename, weight_commcenter, weight_normal, years, \
    set_name_original, set_name_extra, classes, edges_header, edges_format, out_edges_filename

from read import read_global_mapping, read_clasification_mapping, read_coauther, write, string_to_pair
start_time = time.time()


id_map, years_map = read_global_mapping()


year_classification_mapping, year_purity = read_clasification_mapping(id_map)


pairs = read_coauther(id_map)


#
# Output the nodes
#
output = list()
# first output the 6 (hidden) community nodes
starting_id = 66666666
for comm in classes:
    id = starting_id + comm
    timestamp = years
    set = set_name_extra % comm
    output.append((id, timestamp, set, ))
# Then output all the global id's
for global_id, years in years_map.items(): # get all the years this node was in
    # get all the communities this node was in per year
    id = global_id
    timestamp = years
    set = [set_name_original % year_classification_mapping[y][global_id] for y in years]
    output.append((id, timestamp, set, ))
write(output, nodes_header, nodes_format, out_nodes_filename)


#
# Output the edges
#
output = list()
# first output a link to all 6 (hidden) community nodes
# output an seperate edge for each year (resulting in approx 30000 edges)
# if this is to slow we could add the timestamp for each edge to get only 6000 edges (one per author)
weight = weight_commcenter
for global_id, years in years_map.items():
    dst = global_id

    # collect all the communitie sfor each year
    years_per_comm = {c: list() for c in classes}
    for y in years:
        comm_for_this_year = year_classification_mapping[y][global_id]
        years_per_comm[comm_for_this_year].append(y)
    
    for comm, years in years_per_comm.items():
        if len(years) > 0:
            src = starting_id + comm # from the hidden comunity node
            set = set_name_extra % comm
            timestamp = years
            output.append((src, dst, "Directed", timestamp, set, weight))
# Then output all the normal nodes
weight = weight_normal
for pair_str, years in pairs.items():
    a, b = string_to_pair(pair_str)
    src = a
    dst = b
    timestamp = years
    set = set_name_original % 0
    output.append((a, b, "Undirected", timestamp, set, weight))
write(output, edges_header, edges_format, out_edges_filename)
print("completed in %.3f seconds" % (time.time() - start_time))
