import sys
import csv

years = range(2001, 2010)
gt = "text" # graph or text

weight_normal = 1.0
weight_commcenter = 0.01

out_nodes_filename = "nodes.csv"
out_edges_filename = "edges.csv"

edges_header = "Source;Target;Type;Timestamp;Set;Weight"
# Source: source node id
# Target: target node id
# Type: directed/undirected
# Timestamp: array of years this edge is in
# Set: 10=author edge, 2x=community x edge
# Weight: the weight of this edge
edges_format = "%s;%s;%s;%s;%s;%s" #5

nodes_header = "Id;Timestamp;Set"
# Id: the global id
# Timestamp: array of years this node is in
# Set: 10=author node, 2x=community x node
nodes_format = "%s;%s;%s"

#
# Create global id mappings
#
in_filename = "../author_mapping/%s_mapping.txt"
name_id_mapping = dict()  # name -> global_id
year_id_mapping = {y: dict() for y in years} # year,id -> global_id
id_years_mapping = dict()  # global_id -> year
for year in years:
    with open(in_filename % year) as in_file:
        for row in csv.reader(in_file, delimiter=','):
            year_id = int(row[0])
            try:
                name = row[1].strip()
            except:
                print row
                exit()
            
            if name in name_id_mapping:
                global_id = name_id_mapping[name]
                id_years_mapping[global_id].append(year)
            else:
                global_id = len(name_id_mapping)+1
                name_id_mapping[name] = global_id
                id_years_mapping[global_id] = [year]
            
            year_id_mapping[year][year_id] = global_id
            

#
# Load baseline group mapping
#
in_filename = "../%s_pred_label_"+gt+".txt"
year_baseline_mapping = {y: dict() for y in years} # year,global_id -> baseline_comm
for year in years:
    with open(in_filename % year) as in_file:
        year_id = 1
        for row in csv.reader(in_file, delimiter=','):
            global_id = year_id_mapping[year][year_id]
            baseline_comm = int(row[0])
            year_baseline_mapping[year][global_id] = baseline_comm
            year_id += 1

#
# Load our group mapping
#
in_filename = "../%s_pred_label_"+gt+".txt"
year_pred_mapping = {y: dict() for y in years} # year,global_id -> pred_comm
for year in years:
    with open(in_filename % year) as in_file:
        year_id = 1
        for row in csv.reader(in_file, delimiter=','):
            global_id = year_id_mapping[year][year_id]
            pred_comm = int(row[0])
            year_pred_mapping[year][global_id] = pred_comm
            year_id += 1

#
# Check group simularity (Maps our mapping to the most similar baseline mapping)
#
year_comm_mapping = {y: [] for y in years} # year, pred_comm -> baseline_comm
year_purity = {y: [] for y in years} # year -> purity
import itertools
max_similarity = 0.0
for year in years:
    max_matches = 0
    total_authors = len(year_id_mapping[year])
    for c in itertools.combinations(range(0, 5), 6): #brute force 6! = 720
        matches = 0
        for year_id, global_id in year_id_mapping[year].iteritems():
            baseline_comm = year_baseline_mapping[year][global_id]
            pred_comm = year_baseline_mapping[year][global_id]
            matches += c[pred_comm] == baseline_comm
        if matches > max_matches:
            max_matches = matches
            year_comm_mapping[year] = c
    year_purity[year] = max_matches / total_authors
# And replace our mapping with the correct one
year_pred_mapping = {y: dict() for y in years}
for y in years:
    for g_id, pred_com in year_pred_mapping[y].iteritems():
        year_pred_mapping[y][g_id] = year_comm_mapping[y][pred_com]

#
# Merge the adjacent filesets
#
in_filename = "../adjacent/%s_graph.adjlist"
def pair_to_string(gida, gidb):
    return str(gida)+"|"+str(gidb)
def string_to_pair(string):
    return string.split("|")
pair_to_years = dict()
for year in years:
    with open(in_filename % year) as in_file:
        for row in csv.reader(in_file, delimiter=' '):
            src = int(row[0])
            i = 1
            while(row[i]):
                dst = int(row[i])
                
                if src < dst:
                    a = src
                    b = dst
                else:
                    a = dst
                    b = src
                
                #found a pair
                pair_str = pair_to_string(a, b)
                
                if pair_str in pair_to_years:
                    pair_to_years[pair_str].append(year)
                else:
                    pair_to_years[pair_str] = [year]
                
                i += 1


# output function
def write(arr_lst, header, format, to_file):
    with open(to_file, 'w') as out_file:
        out_file.write(header+'\n')
        for arr in arr_list:
            out_file.write((arr % format)+'\n')


#
# Output the nodes
#
output = list()
# first output the 6 (hidden) community nodes
for comm in range(0,5):
    output.append([666000+comm, years, 20+comm])
# Then output all the global id's
for global_id in id_year_mapping:
    # get all the years this node was in
    years = id_years_mapping[global_id]
    # get all the communities this node was in per year
    comms = [10+year_pred_mapping[y][global_id] for y in years] # normalize to baseline communities
    output.append([666000+comm, years, comms])
write(output, nodes_header, node_format, node_file)


#
# Output the edges
#
output = list()
# first output a link to all 6 (hidden) community nodes
# output an seperate edge for each year (resulting in approx 30000 edges)
# if this is to slow we could add the timestamp for each edge to get only 6000 edges (one per author)
weight = weight_commcenter
for g_id, years in id_years_mapping.iteritems():
    dst = g_id
    
    this_auth_comm_years = {c: dict() for c in range(0,5)}
    for y in years:
        # add the year to the correct comunity
        comm_for_this_year = year_pred_mapping[y][g_id]
        this_auth_comm_years[comm_for_this_year].append(y)
    
    for comm, years in this_auth_comm_years.itertools():
        src = 666000+comm
        Set = 20+comm
        timestamp = years
        output.append((src, dst, timestamp, Set, weight))
# Then output all the normal nodes
weight = weight_normal
for pair_str, years in pair_to_years.iteritems():
    a, b = string_to_pair(pair_str)
    output.append((a, b, years, 10, weight))
write(output, nodes_header, node_format, node_file)
