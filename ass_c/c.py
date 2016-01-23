import time
from settings import nodes_header, out_nodes_filename, weight_commcenter, weight_normal, \
    classes, edges_header, out_edges_filename, all_years, starting_extra_id

from read import read_global_mapping, read_clasification_mapping, read_coauther, write, string_to_pair
start_time = time.time()


id_map, years_map = read_global_mapping()


year_classification_mapping, year_purity = read_clasification_mapping(id_map)


pairs = read_coauther(id_map)

def year_array_to_gephi_timestamp(array):
    floats = [str(float(y)) for y in array]
    return '<[' + ', '.join(floats) + ']>'
def values_to_gephi_timstamp_values(years, values):
    return '"<[' + ']; ['.join([str(float(years[i])) + ', ' + str(values[i]) for i in range(0,len(years))]) + ']>"'

#
# Output the nodes
#
output = list()
# first output the 6 (hidden) community nodes
starting_id = 999990
for comm in classes:
    id = starting_id + comm
    timestamp = year_array_to_gephi_timestamp(all_years)
    clazz = values_to_gephi_timstamp_values(all_years, [comm for y in all_years])
    output.append((id, timestamp, clazz, ))
# Then output all the global id's
for global_id, years in years_map.items(): # get all the years this node was in
    # get all the communities this node was in per year
    id = global_id
    timestamp = year_array_to_gephi_timestamp(years)
    clazz = values_to_gephi_timstamp_values(years, [year_classification_mapping[y][global_id] for y in years])
    output.append((id, timestamp, clazz, ))
write(output, nodes_header, out_nodes_filename)


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
            id = starting_extra_id + len(output)
            timestamp = year_array_to_gephi_timestamp(years)
            output.append((src, dst, "Directed", id, timestamp, weight))
# Then output all the normal nodes
weight = weight_normal
id = 1
for pair_str, years in pairs.items():
    a, b = string_to_pair(pair_str)
    src = a
    dst = b
    timestamp = year_array_to_gephi_timestamp(years)
    output.append((a, b, "Undirected", id, timestamp, weight))
    id += 1
write(output, edges_header, out_edges_filename)
print("completed in %.3f seconds" % (time.time() - start_time))
