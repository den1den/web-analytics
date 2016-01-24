import sys
from scipy import sparse
import networkx as nx

for year in range(10):
	community = 'results/' + str(year + 2001) + '_community_'
	for c in range(6):
		mapping = {}
		idx = 0
		infile = community + str(c) + '_baseline.csv'
		fin = open(infile, 'r')
		for line in fin.readlines():
			res = line.strip().split()
			for item in res:
				if not mapping.has_key(item):
					mapping[item] = idx
					idx += 1
		fin.close()

		fin = open(infile, 'r')
		row = []
		col = []
		val = []
		for line in fin.readlines():
			res = line.strip().split()
			if len(res) > 1:
				for i in range(1, len(res)):
					row.append(mapping[res[0]])
					col.append(mapping[res[i]])
					val.append(1)
		fin.close()
		
		G = sparse.coo_matrix((val, (row, col)), shape = (idx, idx))
		M = nx.from_scipy_sparse_matrix(G)
		pr = nx.pagerank(M, alpha=0.9)

		print len(mapping), len(pr)
		inv_map = {v: k for k, v in mapping.items()}
		fout = open('results/' + str(year + 2001) + '_pagerank_baseline' + str(c) + '.txt', 'w')
		for p in range(len(pr)):
			fout.write(str(inv_map[p]) + ':' + str(pr[p]) + '\n')
		fout.close()
