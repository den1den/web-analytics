#!/usr/bin python
from itertools import groupby
from operator import itemgetter
import sys


def count_hashtags_and_date(data):
    def clasifier(obj):
        return obj[0]+' '+obj[1]
    
    for key, group in groupby(data, clasifier):
        try:
            total_count = 0
            for date, tag, count in group:
                total_count += int(count)
            print(''+date+','+tag+','+str(total_count))
        except ValueError as e:
            print >> sys.stderr, 'Reducer error '+str(e)


def count_feel(data):
    def clasifier(obj):
        return str(obj[0])+' '+str(obj[1])
    for key, group in groupby(data, clasifier):
        try:
            total_count = 0
            for a, count in group:
                total_count += int(count)
            print(''+a+',feel,'+','+str(total_count))
        except ValueError as e:
            print >> sys.stderr, 'Reducer error '+str(e)


def read_mapper_output(file, separator='\t'):
    for line in file:
        yield line.rstrip().split(separator)


def main(reducer_function, separator=' '):
    print >> sys.stderr, 'Reducer started'
    data = read_mapper_output(sys.stdin, separator=separator)
    reducer_function(data)
    print >> sys.stderr, 'Reducer completed'


if __name__ == "__main__":
    method_name = sys.argv.pop(1)
    possibles = globals().copy()
    possibles.update(locals())
    method = possibles.get(method_name)
    if not method:
        raise Exception("Method %s not implemented" % method_name)
    main(method)

