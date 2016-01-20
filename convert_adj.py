import sys
import csv

mapping_file = "author_labels/2001_labels.txt"
edges_file = "adjacent/2001_graph.csv"
edges_output = "adjacent/edges" + ".csv"
nodes_output = "adjacent/nodes" + ".csv"

mapping = [line.rstrip('\n') for line in open(mapping_file)]
def get_comm(author_id):
    return label_mapping[author_id-1]

output = list()
with open(edges_file) as in_file:
    output.append("Source;Target;Type")
    for row in csv.reader(in_file, delimiter=';'):
        i = 0
        src = row[i]
        while i < len(row):
            if row[i] and row[i] != src:
                output.append(src + ";" + row[i] + ";Directed" )
            i = i + 1

with open(edges_output, 'w') as out_file:
    out_file.write('\n'.join(output))
output = list()

output.append("Id;Community")
with open(mapping_file) as in_file:
    output.append("Source;Target;Type")
    i = 0
    for row in csv.reader(in_file, delimiter=';'):
        i = i + 1
        o = "%s;%s" % (i, row[0])
        output.append(o)

with open(nodes_output, 'w') as out_file:
    out_file.write('\n'.join(output))
output = []

