from time import time
import numpy as np

from sklearn.cluster import KMeans
from sklearn.preprocessing import scale

def Kmeans_clustering_using_text(featfile, labelfile, predfile):
	np.random.seed(42)

	rawdata = np.loadtxt(featfile)
	labels = np.loadtxt(labelfile)

	#data = scale(rawdata)
	data = rawdata

	n_samples, n_features = data.shape
	n_classes = len(np.unique(labels))

	kmeans = KMeans(init='random', n_clusters=6, n_init=10)
	results = kmeans.fit(data)

	fout = open(predfile, 'w')
	for item in results.labels_:
	  fout.write(str(item) + '\n')
	fout.close()

for i in range(1):
	print 'Clustering the year %d data' % (2001 + i)
	featfile = 'text_features/' + str(2001 + i) + '_text_features.txt'
	labelfile = 'author_labels/' + str(2001 + i) + '_labels.txt'
	predfile = str(2001 + i) + '_pred_label_text.txt'
	Kmeans_clustering_using_text(featfile, labelfile, predfile)

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
		fout = open('results/' + str(2001 + i) + '_community_' + str(idx) + '_text.csv', 'w')
		for item in temp:
			fout.write(item + '\n')
		fout.close()
		idx += 1