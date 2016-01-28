import json
import time
import settings
from settings import all_years, classes

settings.print_purity = False
from read import read_global_mapping, read_clasification_mapping
all_years_min1 = range(2001, 2010)
start_time = time.time()


# id_map[year][id] = g_id
# years_map[g_id] = [year, ...]
id_map, years_map = read_global_mapping()

# classification_mapping[year][global_id] = community
classification_mapping, year_purity = read_clasification_mapping(id_map)

totals = {
    y: {COMM: len([ids for ids, comm in classification_mapping[y].items() if comm == COMM]) for COMM in classes}
    for y in all_years
}

table = {y: {} for y in all_years_min1}
n_statatisitcs = 6

for comm in settings.classes:
    for year_a in all_years_min1:  # 2001 - 2009
        year_b = year_a + 1

        quitters = 0        # comm -> no listing
        stayers = 0         # comm -> comm
        switched_out = 0    # comm -> other comm
        switched_in = 0     # other comm -> comm
        returnee = 0        # no listing previous year -> comm
        new_commers = 0     # no listing any prev year -> comm

        for author, old_comm in classification_mapping[year_a].items():
            if old_comm == comm:
                # This author is from the previous year and this previous community

                if not author in classification_mapping[year_b]:
                    quitters += 1
                else:
                    # it is also in a community the next year
                    next_comm =  classification_mapping[year_b][author]

                    # comm is the community in the previous year
                    if next_comm == comm:
                        # this author has been in the same community
                        stayers += 1
                    else:
                        # this auther has switched from comm to curr_comm
                        switched_out += 1

        for author, new_comm in classification_mapping[year_b].items():
            # This author is from the next year and has a community
            if new_comm == comm:
                # it has the same community now

                if author not in classification_mapping[year_a]:
                    # did not exist in previous year
                    first_apperance_year = min(years_map[author])
                    if first_apperance_year < year_a:
                        returnee += 1
                    else:
                        new_commers += 1
                elif classification_mapping[year_a][author] != comm:
                    # the author had a different community last year
                    switched_in += 1
                else:
                    #this author was in the same community last year so
                    pass

        table[year_a][comm] = (quitters, stayers, switched_out, switched_in, new_commers, returnee)
        assert len(table[year_a][comm]) == n_statatisitcs

def get_label_c(year, community):
    return "%s (%s)" % (year, community)
def get_label_d(year):
    return "%s Gone" % year

sankey = []
for y in all_years_min1:
    y2 = y + 1
    for commA in classes:
        for commB in classes:
            n = len([gid
                     for gid, comm
                     in classification_mapping[y].items()
                     if (comm == commA
                         and gid in classification_mapping[y2]
                         and classification_mapping[y2][gid] == commB)])
            sankey.append((get_label_c(y, commA), get_label_c(y2, commB), n, ))
        n = len([gid
                 for gid, comm
                 in classification_mapping[y].items()
                 if (comm == commA
                     and gid not in classification_mapping[y2])])
        sankey.append((get_label_c(y, commA), get_label_d(y2), n, ))
        n = len([gid
                 for gid, comm
                 in classification_mapping[y2].items()
                 if (comm == commA
                     and gid not in classification_mapping[y])])
        sankey.append((get_label_d(y), get_label_c(y2, commA), n, ))


output = open('3/3_output.html', 'w')

print('<table>'
      '<h1>Number of individual authors</h1>'
      '<thead><tr>'
      '<td>Community</td>'
      '<td>Type</td>', file=output)
for y in all_years_min1:
    print('<td>%s -> %s</td>' % (y, y + 1), file=output)
print('</tr></thead>', file=output)

print('<tbody>', file=output)
for row_i in range(n_statatisitcs * len(settings.classes)):
    print('<tr>', file=output)
    comm = int(row_i / n_statatisitcs)
    print('<td>%s</td>' % comm, file=output)
    val = row_i % n_statatisitcs
    print('<td>%s</td>' % ['Quit', 'Stay', 'Switch Out', 'Switch In', 'New', 'Returnee'][val], file=output)
    for y in all_years_min1:
        print('<td>%s</td>' % table[y][comm][val], file=output)
    print('</tr>', file=output)
print('</tbody></table>', file=output)

print("<p>"
      "Quit: comm -> no listing<br/>"
      "Stay: comm -> comm<br/>"
      "Switch In: other comm -> comm<br/>"
      "Switch Out: comm -> other comm<br/>"
      "New: no listing in any prev year -> comm<br/>"
      "Returnee: a listing in some prev year (for some community) -> comm"
      "</p>", file=output)

print("<h2>Totals</h2>", file=output)
#print("<pre>%s</pre>" % str(totals).replace(',', '\n').replace(':', '\n').replace('{','').replace('}',''), file=output)
print("<pre>%s</pre>" % str(totals).replace(', ', ', \n'), file=output)

output2 = open("3/sankey-data.js", 'w')
print("var data = %s;" % json.dumps(sankey).replace('], [','],\n['), file=output2)

print("Output is written to "+str(output.name)+" and "+str(output2))
print("completed in %.3f seconds" % (time.time() - start_time))