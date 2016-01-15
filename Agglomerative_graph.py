import numpy as np

from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import scale

def Agglomerative_clustering_using_graph(featfile, labelfile, predfile):
	rawdata = np.loadtxt(featfile)
	labels = np.loadtxt(labelfile)

	data = scale(rawdata)
	X = data
	y = labels

	n_samples, n_features = X.shape

	np.random.seed(0)

	clustering = AgglomerativeClustering(n_clusters=6)
	res = clustering.fit(X)

	fout = open(predfile, 'w')
	for item in res.labels_:
	    fout.write(str(item) + '\n')
	fout.close()

for i in range(10):
	print 'Clustering the year %d data' % (2001 + i)
	featfile = 'graph_features/' + str(2001 + i) + '_graph_features.txt'
	labelfile = 'author_labels/' + str(2001 + i) + '_labels.txt'
	predfile = str(2001 + i) + '_pred_label_graph.txt'
	Agglomerative_clustering_using_graph(featfile, labelfile, predfile)

	fin = open(predfile, 'r')
	comms = [set() for t in range(6)]
	idx = 1
	for line in fin.readlines():
		comms[int(line.strip())].add(idx)
		idx += 1
	fin.close()

	adjfile = 'adjacent/' + str(2001 + i) + '_graph.adjlist'
	idx = 0
	for iset in comms:
		temp = []
		fin = open(adjfile, 'r')
		for line in fin.readlines():
			s = ''
			tmp = line.strip().split()
			for item in tmp:
				if int(item) in iset:
					s += item + ' '
			if len(s) > 1:
				temp.append(s)
		fin.close()
		fout = open('results/' + str(2001 + i) + '_community_' + str(idx) + '_graph.csv', 'w')
		for item in temp:
			fout.write(item + '\n')
		fout.close()
		idx += 1