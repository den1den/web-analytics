for i in range(10):
	print 'Clustering the year %d data for baseline' % (2001 + i)
	labelfile = 'author_labels/' + str(2001 + i) + '_labels.txt'

	fin = open(labelfile, 'r')
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
		fout = open('results/' + str(2001 + i) + '_community_' + str(idx) + '_baseline.csv', 'w')
		for item in temp:
			fout.write(item + '\n')
		fout.close()
		idx += 1
