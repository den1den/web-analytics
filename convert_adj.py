import sys
import csv

mapping_file = "author_labels/2001_labels.txt"
edges_file = "adjacent/2001_graph.csv"
edges_output = "adjacent/edges" + ".csv"
nodes_output = "adjacent/nodes" + ".csv"

inter_weight = 0.01
intra_weight = 1.0

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
output.append("Source;Target;Type;Weight")
with open(edges_file) as in_file:
    for row in csv.reader(in_file, delimiter=';'):
        i = 0
        src = row[i]
        while i < len(row):
            dst = row[i]
            if dst and dst != src:
                if get_comm(int(src)) == get_comm(int(dst)):
                    weight = intra_weight
                else:
                    weight = inter_weight
                output.append("%s;%s;%s;%s" % (
                    src,
                    dst,
                    "Directed",
                    weight,
                ))
            i = i + 1

with open(edges_output, 'w') as out_file:
    out_file.write('\n'.join(output))

