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
#starts_tweet = re.compile(r'^\d{1,},')
is_header = re.compile(r'^ID,USER_ID,USER_NAME,SOURCE,TEXT,CREATED,FAVORITED,RETWEET,RETWEET_COUNT,RETWEET_BY_ME,POSSIBLY_SENSITIVE,GEO_LATITUDE,GEO_LONGITUDE,LANGUAGE_CODE,PLACE,PLACE_TYPE,PLACE_URL,STREET_ADDRESS,COUNTRY,COUNTRY_CODE,IN_REPLY_TO_STATUS_ID,IN_REPLY_TO_USER_ID,RETWEETED_STATUS_ID,RETWEETED_STATUS_USER_ID,RETWEETED_STATUS_CREATED,EXPANDED_URLS$')
find_hashtag = re.compile(r'[^&]#(\S+)')
logger = logging.getLogger('')

class Reader:
    #init
    line_number = 0
    tweet_number = 0
    single_hastags = 0
    skipped = []
    annomalies = []
    last_ended_quote = ()
    
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
        line = self.skip_until_tweet()
        
        #inv: line contains the next tweet
        
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
                arr = arr[tweet_data_length:]
                self.mapper(tweet)
            
            line = self.next_line()
        
        print >> sys.stderr, 'Mapping done: {0} tweets found, {1} tweets skipped, {2} lines read, {3} single hashtags found'.format(
            self.tweet_number,
            len(self.skipped),
            self.line_number,
            self.single_hastags,
        )


    def mapper(self, data):
        if len(data) != 26:
            raise ValueError("Entry has wrong length")
        try:
            float(data[0])
        except ValueError:
            raise ValueError("Entry has no id")
        
        hashtags = list()
        try:
            words = data[4].strip()
            date = data[5].strip()
            date = date[:-9]
            hashtags = find_hashtag.findall(words)
            self.tweet_number += 1
        except Exception as e:
            self.skipped += e
            pass
        if hashtags:
            for tag in hashtags:
                if len(tag) == 1:
                    self.single_hastags += 1
                print tag, 1


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
    if len(sys.argv) > 1 and sys.argv.pop(1)=="test":
        # python ./mapper.py test
        unittest.main()
    else:
        Reader().run()

