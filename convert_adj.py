import sys
import csv
with open(sys.argv[1]) as infile:
    print("Source;Target;Type")
    for row in csv.reader(infile, delimiter=';'):
        i = 0
        src = row[i]
        while i < len(row):
            if row[i] and row[i] != src:
                print(src + ";" + row[i] + ";" + "Directed")
            i = i + 1

