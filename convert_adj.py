import sys
import csv

mapping_file = "author_labels/2001_labels.txt"
edges_file = "adjacent/2001_graph.csv"
edges_output = "adjacent/edges" + ".csv"
edges_n2_output = "adjacent/edges_n2" + ".csv"
nodes_output = "adjacent/nodes" + ".csv"

inter_weight = 1.0
intra_weight = 1.0

extra_edges_weight = 0.001

print "started normal"
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

# Write extra interconnected lines between all nodes of same cummunity (this is a very large file and contains O(n^2) entries)
print "started n2"
output = list()
output.append("Source;Target;Weight")
output_format = "%s" + ';' + "%s" + ';' + str(extra_edges_weight)
comms = {'0': list(), '1': list(), '2': list(), '3': list(), '4': list(), '5': list()}
id = 1
while id <= len(mapping):
    comms[mapping[id-1]].append(id)
    id = id + 1
for comm_id, commlist in comms.iteritems():
    for auth_id in commlist:
        for other_auth in commlist:
            if auth_id != other_auth:
                output.append(output_format % (auth_id, other_auth))
print sum([len(v)*(len(v)-1) for v in comms.itervalues()])

print "Printing lines"
with open(edges_n2_output, 'w') as out_file:
    out_file.write('\n'.join(output))
