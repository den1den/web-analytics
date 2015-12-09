#!/usr/bin/env python

import sys
import csv
import re

data_initial = open("tweets", "rU")
data = csv.reader((line.replace('\0','') for line in data_initial), delimiter=",")

for line in data:
	try:
		words = line[4].strip()
		date = line[5].strip()
		date = date[:-9]
		hashtags = re.findall(r"#(\w+)", words)
		for tag in hashtags:
        		print tag, 1
	except:
		pass
		
