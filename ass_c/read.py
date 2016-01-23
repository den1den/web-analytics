import csv
from settings import years, filenames, purity_classification_group_mapping


def read_global_mapping():
    name_map = dict()
    id_map = {y: dict() for y in years}
    years_map = dict()

    for year in years:
        with open(filenames['author_mapping'] % year) as in_file:
            for row in csv.reader(in_file, delimiter=','):
                id = int(row[0])
                name = row[1].strip()

                if name in name_map:
                    # already known
                    g_id = name_map[name]
                    years_map[g_id].append(year)
                else:
                    g_id = len(name_map)+1
                    name_map[name] = g_id
                    years_map[g_id] = [year, ]
                id_map[year][id] = g_id
    return id_map, years_map


def read_clasification_mapping(id_map):
    year_baseline_mapping = {y: dict() for y in years} # year,global_id -> baseline_comm
    for year in years:
        with open(filenames['baseline_labels'] % year) as in_file:
            id = 1
            for row in csv.reader(in_file, delimiter=','):
                global_id = id_map[year][id]
                baseline_comm = int(row[0])
                year_baseline_mapping[year][global_id] = baseline_comm
                id += 1
    year_prediction_mapping = {y: dict() for y in years} # year,global_id -> classification
    for year in years:
        with open(filenames['prediction_labels'] % year) as in_file:
            id = 1
            for row in csv.reader(in_file, delimiter=','):
                global_id = id_map[year][id]
                pred_comm = int(row[0])
                year_prediction_mapping[year][global_id] = pred_comm
                id += 1
    # Check group simularity (Maps our mapping to the most similar baseline mapping)
    classification_group_mapping = {y: dict() for y in years}  # year, pred_comm -> baseline_comm
    year_purity = {y: [] for y in years} # year -> purity
    for year in years:
        max_matches = 0
        for c in purity_classification_group_mapping[year]:  # brute force 6! = 720
            matches = 0
            for id, global_id in id_map[year].items():
                baseline_comm = year_baseline_mapping[year][global_id]
                pred_comm = year_prediction_mapping[year][global_id]
                matches += c[pred_comm] == baseline_comm
            if matches > max_matches:
                max_matches = matches
                classification_group_mapping[year] = c

        total_authors = len(id_map[year])
        year_purity[year] = max_matches / total_authors
        print("%s got a purity of %0.3f in year %s" % (classification_group_mapping[year], year_purity[year], year))

    # And replace our mapping with the correct one
    year_classification_mapping = {y: dict() for y in years}
    for y in years:
        for g_id, pred_com in year_prediction_mapping[y].items():
            year_classification_mapping[y][g_id] = classification_group_mapping[y][pred_com]

    return year_classification_mapping, year_purity


def pair_to_string(a, b):
    return str(a)+"|"+str(b)


def string_to_pair(s):
    return s.split("|")


def read_coauther(id_map):
    pairs = dict()
    for year in years:
        with open(filenames['coauthor'] % year) as in_file:
            for row in csv.reader(in_file, delimiter=' '):
                src = id_map[year][int(row[0])]
                i = 1
                while row[i]:
                    dst = id_map[year][int(row[i])]

                    if src < dst:
                        a = src
                        b = dst
                    else:
                        a = dst
                        b = src

                    #found a pair
                    pair_str = pair_to_string(a, b)

                    if pair_str in pairs:
                        pairs[pair_str].append(year)
                    else:
                        pairs[pair_str] = [year, ]

                    i += 1
    return pairs


def write(arr_list, header, format, to_file):
    with open(to_file, 'w') as out_file:
        out_file.write(header+'\n')
        for arr in arr_list:
            out_file.write((format % arr)+'\n')

