#!/usr/bin python
import sys
import csv
import re
import unittest
import logging

#constants
tweet_data_length = 26
starts_quote = re.compile(r'.*,"(""|[^"])*$')
ends_quote = re.compile(r'^(""|[^"])*"([^"].*|)$')
starts_tweet = re.compile(r'^\d{3,},')
starts_tweet = re.compile(r'^\d{1,},')
is_header = re.compile(r'^ID,USER_ID,USER_NAME,SOURCE,TEXT,CREATED,FAVORITED,RETWEET,RETWEET_COUNT,RETWEET_BY_ME,POSSIBLY_SENSITIVE,GEO_LATITUDE,GEO_LONGITUDE,LANGUAGE_CODE,PLACE,PLACE_TYPE,PLACE_URL,STREET_ADDRESS,COUNTRY,COUNTRY_CODE,IN_REPLY_TO_STATUS_ID,IN_REPLY_TO_USER_ID,RETWEETED_STATUS_ID,RETWEETED_STATUS_USER_ID,RETWEETED_STATUS_CREATED,EXPANDED_URLS$')
find_hashtag = re.compile(r'[^&]#([\w|\d+]{2,})')
logger = logging.getLogger('')
i_feel = re.compile(r'(\w+) feel (\w+)', re.IGNORECASE)
feel_re = re.compile(r'I feel ([\w\s])+', re.IGNORECASE)
feel_3wrds = re.compile(r'I\s+feel\s+([#\w]+)\s*([#\w]+)?\s*([#\w]+)?', re.IGNORECASE)
feel_positive = re.compile(r'i\s+feel(\s+|(?:very)|(?:so)|(?:like)|(?:rly)|(?:real+y)|(?:super))*\s+((?:goo+d)|(?:happy)|(?:fine)|(?:excited))', re.IGNORECASE)
feel_negative = re.compile(r'i\s+feel(\s+|(?:very)|(?:so)|(?:like)|(?:rly)|(?:real+y)|(?:super))*\s+((?:shit)|(?:bad)|(?:sad)|(?:lonely)|(?:disap+ointed)|(?:ter+ible))', re.IGNORECASE)
is_date = re.compile(r'\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d')

#this function can be used by calling with 'python mapper.py count_hashtags'
def count_hashtags(data):
    try:
        words = data[4].strip()
        hashtags = find_hashtag.findall(words)
    except Exception as e:
        return e
    if hashtags:
        for tag in hashtags:
            print tag, 1
    return 1


def count_hashtags_and_date(data):
    try:
        words = data[4].strip()
        date = data[5].strip()
        date = date[:-9]
        hashtags = find_hashtag.findall(words)
    except Exception as e:
        return e
    if hashtags:
        for tag in hashtags:
            print date, tag, 1
    return 1


def count_feel(data):
    try:
        words = data[4].strip()
        date = data[5].strip()
        date = date[:-9]
        grps = i_feel.findall(words)
    except Exception as e:
        return e
    if grps:
        for grp in grps:
            print grp[0], 'feel', grp[1], 1
    return 1


def output_feel(data):
    try:
        words = data[4].strip()
        positive_groups = feel_positive.findall(words)
        negative_groups = feel_negative.findall(words)
    except Exception as e:
        return e
    if positive_groups:
        for grps in positive_groups:
            if len(grps) == 2:
                print grps[0], grps[1], '1', 1
            else:
                print "MATCHING_ERROR", str(len(grps)), 1
    if negative_groups:
        for grps in negative_groups:
            if len(grps) == 2:
                print grps[0], grps[1], '0', 1
            else:
                print "MATCHING_ERROR", str(len(grps)), 1
    return 1


def smileys(data):
    try:
        tweet = data[4].strip()
        date = data[5].strip()
        if not is_date.match(date):
            print >> sys.stderr, 'Non date found in date field: '+str(date)
            return 0
        date = date[:10]+'_'+date[11:16]
        if not date:
            data = "UNDEFINED"
        
        emotweets = []
        if ":)" in tweet:
            emotweets.append(":)")
        elif ":(" in tweet:
            emotweets.append(":(")
        elif "happy" in tweet:
            emotweets.append("happy")
        elif "sad" in tweet:
            emotweets.append("sad")
        elif "lonely" in tweet:
            emotweets.append("lonely")
        elif "XD" in tweet:
            emotweets.append("XD")
        
        #done, print outcome
        for emotweet in emotweets:
            print emotweet, date, "1"
        return 1
    except Exception as e:
        return e


class Reader:
    #init
    line_number = 0
    tweet_number = 0
    single_hastags = 0
    skipped = []
    
    
    def __init__(self, function):
        self.function = function
    
    
    def next_line(self):
        self.line_number += 1
        return sys.stdin.readline()
    
    
    def skip_until_tweet(self):
        line = self.next_line()
        if line:
            if is_header.match(line):
                return self.next_line()
            while line and not starts_tweet.match(line):
                #search for the first tweet start
                line = self.next_line()
        return line
    
    
    def run(self):
        #inv: line contains the next tweet
        line = self.skip_until_tweet()
        arr = []
        #the loop
        while line:
            line = line.replace('\0', '').replace('\n', '').replace('\r', '')
            try:
                nxt = next(csv.reader([line], delimiter=",", quotechar='"'))
            except Exception as e:
                print >> sys.stderr, 'CSV error while parsing line '+str(line)
                raise e
            
            while len(arr)+len(nxt) < tweet_data_length:
                # expand the line
                next_line = self.next_line()
                if not next_line:
                    #EOF
                    break
                next_line = next_line.replace('\0', '').replace('\n', '').replace('\r', '')
                line += next_line
                nxt = next(csv.reader([line], delimiter=",", quotechar='"'))
            arr += nxt
            
            # at least one tweet is in arr
            while len(arr) >= tweet_data_length:
                tweet = arr[:tweet_data_length]
                if len(tweet) != 26:
                    raise ValueError("Entry has wrong length")
                try:
                    float(tweet[0])
                except ValueError:
                    raise ValueError("Entry has no id")
                result = self.function(tweet)
                if type(result) == int:
                    self.tweet_number += result
                else:
                    self.skipped += result
                arr = arr[tweet_data_length:]
            line = self.next_line()
        if len(self.skipped) == 0:
            print >> sys.stderr, 'Mapping done: {0} tweets found, {1} tweets skipped, {2} lines read, {3} single hashtags found'.format(
                self.tweet_number,
                len(self.skipped),
                self.line_number,
                self.single_hastags,
            )
        else:
            print >> sys.stderr, 'Mapping failed: {0} tweets found, {1} tweets skipped, {2} lines read, {3} single hashtags found'.format(
                self.tweet_number,
                len(self.skipped),
                self.line_number,
                self.single_hastags,
            )
            for e in self.skipped:
                print >> sys.stderr, e


class Test(unittest.TestCase):


    def do_test(self, string, exp, first_group=None):
        result = self.regex.match(string)
        if result:
            self.assertEqual(True, exp)
            if first_group is not None:
                self.assertEqual(result.group(1), first_group)
        else:
            self.assertEqual(False, exp)
    
    
    def test_regex(self):
        self.regex = starts_quote
        self.do_test('', False)
        self.do_test('x,', False)
        self.do_test(',"', True)
        self.do_test('x,"', True)
        
        self.do_test('x,"""', True)
        self.do_test('x,"""', True)
        self.do_test('x,"""""', True)
        self.do_test('x,"x""', True)
        
        self.do_test('x,"x', True)
        self.do_test('x,",', True)
        # x,x" is invalid
        
        self.regex = starts_tweet
        self.do_test('', False)
        self.do_test('414349810221588480,415066297', True)
        self.do_test('00:01:07,', False)
        self.do_test('00000000!0000,"', False)
        self.do_test(',', False)
        
        self.regex = ends_quote
        self.do_test('', False)
        self.do_test('"', True, '')
        self.do_test('",""', True, '')
        self.do_test('","', True, '')
        self.do_test('x', False)
        self.do_test('x"', True, 'x')
        self.do_test('x",""', True, 'x')
        self.do_test('x","', True, 'x')
        
        self.do_test('"",', False)
        self.do_test('"","', True, '"",')
        self.do_test('"""', True, '""')
        self.do_test('""","', True, '""')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg = sys.argv.pop(1)
        if arg == "test":
            unittest.main()
        else:
            method_name = arg
            possibles = globals().copy()
            possibles.update(locals())
            method = possibles.get(method_name)
            if not method:
                raise Exception("Method %s not implemented" % method_name)
            Reader(method).run()

