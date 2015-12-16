#!/usr/bin python
"""A more advanced Reducer, using Python iterators and generators."""

from itertools import groupby
from operator import itemgetter
import sys

def read_mapper_output(file, separator='\t'):
    for line in file:
        yield line.rstrip().split(separator, 1)

def main(separator=' '):
    # input comes from STDIN (standard input)
    data = read_mapper_output(sys.stdin, separator=separator)
    # groupby groups multiple word-count pairs by word,
    # and creates an iterator that returns consecutive keys and their group:
    #   current_word - string containing a word (the key)
    #   group - iterator yielding all ["&lt;current_word&gt;", "&lt;count&gt;"] items
    for current_word, group in groupby(data, itemgetter(0)):
        try:
            total_count = sum(int(count) for current_word, count in group)
            print('"'+current_word+'",'+str(total_count))
        except ValueError as e:
            print >> sys.stderr, 'Reducer error '+str(e)


def count_hashtags_and_date(data):
    def clasifier(obj):
        return obj[0]+' '+obj[1]
    
    for key, group in groupby(data, clasifier):
        try:
            total_count = 0
            for date, tag, count in group:
                total_count += int(count)
            print(''+date+',"'+tag+'",'+str(total_count))
        except ValueError as e:
            print >> sys.stderr, 'Reducer error '+str(e)


def count_feel(data):
    def clasifier(obj):
        return obj[0]+' '+obj[1]
    for key, group in groupby(data, clasifier):
        try:
            total_count = 0
            for pre, post, count in group:
                total_count += int(count)
            print(''+pre+',"feel","'+post+'",'+str(total_count))
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
    main()
