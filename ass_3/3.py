import time
import settings
settings.print_purity = False
from read import read_global_mapping, read_clasification_mapping
all_years_min1 = range(2001, 2010)
start_time = time.time()


# id_map[year][id] = g_id
# years_map[g_id] = [year, ...]
id_map, years_map = read_global_mapping()

# classification_mapping[year][global_id] = community
classification_mapping, year_purity = read_clasification_mapping(id_map)

table = {y: {} for y in all_years_min1}

for comm in settings.classes:
    for year_a in all_years_min1:  # 2001 - 2009
        year_b = year_a + 1

        quitters = 0        # comm -> no listing
        stayers = 0         # comm -> comm
        switched_out = 0    # comm -> other comm
        switched_in = 0     # other comm -> comm
        new_commers = 0     # no listing -> comm

        authors_in_year_a = list()

        for _dummy, author in id_map[year_a].items():
            authors_in_year_a.append(author)

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

        for _dummy, author in id_map[year_b].items():
            # for each author in the next year
            if author not in authors_in_year_a:
                # This is a new author
                new_commers += 1
            else:
                # The auther was already in year a
                prev_comm = classification_mapping[year_a][author]
                if prev_comm == comm:
                    # This author has been in the same community (and is already counted)
                    pass
                else:
                    # this author has switched from prev_comm to comm
                    switched_in += 1

        table[year_a][comm] = (quitters, stayers, switched_out, switched_in, new_commers, )


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
for row_i in range(5 * len(settings.classes)):
    print('<tr>', file=output)
    comm = int(row_i / 5)
    print('<td>%s</td>' % comm, file=output)
    val = row_i % 5
    print('<td>%s</td>' % ['Quit', 'Stay', 'Switch In', 'Switch Out', 'New'][val], file=output)
    for y in all_years_min1:
        print('<td>%s</td>' % table[y][comm][val], file=output)
    print('</tr>', file=output)
print('</tbody></table>', file=output)

print("<p>Quit: comm -> no listing<br/>Stay: comm -> comm<br/>Switch In: other comm -> comm<br/>"
      "Switch Out: comm -> other comm<br/>New: no listing -> comm</p>", file=output)

print("Output is written to "+str(output.name))
print("completed in %.3f seconds" % (time.time() - start_time))