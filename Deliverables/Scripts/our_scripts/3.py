import time
from read import read_global_mapping
from settings import all_years

start_time = time.time()


# id_map[year][id] = g_id
# years_map[g_id] = [year, ...]
id_map, years_map = read_global_mapping()

new_authors = {y: 0 for y in all_years}
left_authors = {y: [0 for y in all_years] for y in all_years}

new_authors[all_years[0]] = len(id_map[all_years[0]])

