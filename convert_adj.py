import sys
import csv

mapping_file = "author_labels/2001_labels.txt"
edges_file = "adjacent/2001_graph.csv"
edges_output = "adjacent/edges" + ".csv"
nodes_output = "adjacent/nodes" + ".csv"
edges_2_output = "adjacent/edges_commlink" + ".csv"

weight_default = 1.0
weight_commedge = 0.001

mapping = [line.rstrip('\n') for line in open(mapping_file)]
def get_comm(author_id):
    return mapping[author_id-1]


output = list()
output.append("Id;Community")
with open(mapping_file) as in_file:
    i = 0
    for row in csv.reader(in_file, delimiter=';'):
        i = i + 1
        o = "%s;%s" % (i, row[0])
        output.append(o)
with open(nodes_output, 'w') as out_file:
    out_file.write('\n'.join(output))


output = list()
output.append("Source;Target;Type;Weight;CommLink")
output_format = "%s;%s;Directed;%s;50"
with open(edges_file) as in_file:
    for row in csv.reader(in_file, delimiter=';'):
        i = 0
        src = row[i]
        while i < len(row):
            dst = row[i]
            if dst and dst != src:
                weight = weight_default
                output.append(output_format % (
                    src,
                    dst,
                    weight,
                ))
            i = i + 1
with open(edges_output, 'w') as out_file:
    out_file.write('\n'.join(output))

# Write extra interconnected lines between all nodes of same cummunity (this is a very large file and contains O(n^2) entries)
output = list()
output.append("Source;Target;Type;Weight;CommLink")
output_format = "%s;%s;Directed;" + str(weight_commedge) + ";%s"
comms = {'0': list(), '1': list(), '2': list(), '3': list(), '4': list(), '5': list()}
id = 1
while id <= len(mapping):
    comms[mapping[id-1]].append(id)
    id = id + 1
for comm_id, commlist in comms.iteritems():
    src = 10000 + int(comm_id)
    for authorid in commlist:
        dst = authorid
        output.append(output_format % (
            src,
            dst,
            int(comm_id)+10,
        ))
with open(edges_2_output, 'w') as out_file:
    out_file.write('\n'.join(output))

