import sys
import csv

years = range(2001, 2010)
in_filename = "%s_mapping.txt"
out_filename = "global_mapping.csv"
# Output format: year;id;global_id;name
output_format = "%s;%s;%s;%s"

i = 0;

output = list()
mapping = dict()  # mapping from name -> global_id
for year in years:
    with open(in_filename % year) as in_file:
        for row in csv.reader(in_file, delimiter=','):
            year_id = int(row[0])
            name = row[1].strip()
            
            if name in mapping:
                global_id = mapping[name]
            else:
                global_id = len(mapping)+1
                mapping[name] = global_id
            
            output.append(output_format % (year, year_id, global_id, name))
            
            if i > 10:
                break
print output
exit()
with open(out_filename, 'w') as out_file:
    out_file.write('\n'.join(output))

# Test opening of the file and put it in mapping (year, year_id) -> (global_id)
with open(out_filename) as in_file:
    year_mapping = {y: dict() for y in years}
    for row in csv.reader(in_file, delimiter=';'):
        year = int(row[0])
        year_id = int(row[1])
        global_id = int(row[2])
        year_mapping[year][year_id] = global_id

