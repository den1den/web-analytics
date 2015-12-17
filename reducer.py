#!/usr/bin python
from itertools import groupby
from operator import itemgetter
import sys


minimal_freq = 2


def count_hashtags(data):
    # groupby groups multiple word-count pairs by word,
    # and creates an iterator that returns consecutive keys and their group:
    #   current_word - string containing a word (the key)
    #   group - iterator yielding all ["&lt;current_word&gt;", "&lt;count&gt;"] items
    for current_word, group in groupby(data, itemgetter(0)):
        try:
            total_count = sum(int(count) for current_word, count in group)
            if total_count >= minimal_freq:
                print(''+current_word+','+str(total_count)+'')
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
            print(''+date+','+tag+','+str(total_count))
        except ValueError as e:
            print >> sys.stderr, 'Reducer error '+str(e)


def prepost_feel(data):
    def clasifier(obj):
        return str(obj[0])+' '+str(obj[1])
    for key, group in groupby(data, clasifier):
        try:
            total_count = 0
            for pre, post, count in group:
                total_count += int(count)
            print(''+pre+',feel,'+post+','+str(total_count))
        except ValueError as e:
            print >> sys.stderr, 'Reducer error '+str(e)


def output_feel(data):
    def clasifier(obj):
        return obj[0]+obj[1]+obj[2]
    for key, group in groupby(data, clasifier):
        try:
            total_count = 0
            for bvg, znm, gorb, count in group:
                total_count += int(count)
            print(str(total_count)+','+gorb+','+bvg+','+znm+'')
        except ValueError as e:
            print >> sys.stderr, 'Reducer error on '+str(group)+', '+str(e)


def user_freq(data):
    def clasifier(obj):
        #calisify on usrid and tag
        return obj[0]+obj[2]
    
    for key, group in groupby(data, clasifier):
        try:
            total_count = 0
            for userid, username, hashtag, count in group:
                total_count += int(count)
            username.replace(',','_')
            print(''+userid+','+hashtag+','+str(total_count))
        except ValueError as e:
            print >> sys.stderr, 'Reducer error '+str(e)


def tweet_intensity(data):
    def clasifier(obj):
        #calisify on date only
        return obj[0]
    
    for key, group in groupby(data, clasifier):
        try:
            total_count = 0
            for date, count in group:
                total_count += int(count)
            print(''+date.replace('_',' ')+':00,'+str(total_count))
        except ValueError as e:
            print >> sys.stderr, 'Reducer error '+str(e)


def smileys(data):
    def clasifier(obj):
        return obj[0]+obj[1]
    for key, group in groupby(data, clasifier):
        try:
            total_count = 0
            for emo, minute, count in group:
                total_count += int(count)
            print(''+minute.replace('_',',')+':00,'+emo+','+str(total_count))
        except ValueError as e:
            print >> sys.stderr, 'Reducer error on '+str(group)+', '+str(e)


def read_mapper_output(file):
    separator=' '
    for line in file:
        yield line.rstrip().split(separator)


def main(reducer_function):
    print >> sys.stderr, 'Reducer started'
    data = read_mapper_output(sys.stdin)
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

