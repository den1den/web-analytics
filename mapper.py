#!/usr/bin python
import sys
import csv
import re
import unittest

#constants
tweet_data_length = 26
starts_quote = re.compile(r'.*,"(""|[^"])*$')
ends_quote = re.compile(r'^(""|[^"])*"([^"].*|)$')
starts_tweet = re.compile(r'^\d{3,},')
is_header = re.compile(r'^ID,USER_ID,USER_NAME,SOURCE,TEXT,CREATED,FAVORITED,RETWEET,RETWEET_COUNT,RETWEET_BY_ME,POSSIBLY_SENSITIVE,GEO_LATITUDE,GEO_LONGITUDE,LANGUAGE_CODE,PLACE,PLACE_TYPE,PLACE_URL,STREET_ADDRESS,COUNTRY,COUNTRY_CODE,IN_REPLY_TO_STATUS_ID,IN_REPLY_TO_USER_ID,RETWEETED_STATUS_ID,RETWEETED_STATUS_USER_ID,RETWEETED_STATUS_CREATED,EXPANDED_URLS$')

class Reader:
    #init
    line_number = 0
    tweet_number = 0
    skipped = []
    annomalies = []
    last_ended_quote = ()
    
    def next_line(self):
        self.line_number += 1
        return sys.stdin.readline()
    
    def run(self):
        line = self.next_line()
        if not line:
            #empty input
            return
        
        if is_header.match(line):
            #skip the header
            line = self.next_line()
        else:
            while not starts_tweet.match(line):
                #search for the first tweet start
                line = self.next_line()
                if not line:
                    #no header or starting tweet found
                    return
        
        arr = []
        #the loop
        while line:
            line = line.replace('\0', '').replace('\n', '').replace('\r', '')
            
            arr += next(csv.reader([line], delimiter=",", quotechar='"'))
            
            if len(arr) == 0:
                self.annomalies += ('newline before tweet', self.line_number)
                arr = [""]
            
            if len(arr) < tweet_data_length:
                # tweet is acros multiple lines
                # append lines until `arr` becomes large enough
                
                while len(arr) < tweet_data_length:
                    next_line = self.next_line()
                    if not next_line: return #EOF
                    
                    if starts_quote.match(line):
                        # force the closement of the quoted area
                        
                        if ends_quote(next_line):
                            # force the start of the quoted area at the new line
                            next_line = '"' + next_line
                        else:
                            next_line = '"' + next_line + '"'
                    else:
                        arr.append("")
                    
                    next_line = next_line.replace('\0', '')\
                        .replace('\n', '').replace('\r', '')
                    nxt = next(csv.reader([next_line], delimiter=",", quotechar='"'))
                    
                    if len(nxt) == 0:
                        #nothing found, continue searching
                        pass
                    else:
                        arr[-1] += nxt[0]  # append last entry with first of the new line
                        arr += nxt[1:]  # append the rest
                
                #more added then needed
                if len(arr) > tweet_data_length:
                    
            
            if len(arr) > tweet_data_length:
                ln = self.line_number
                # check remaining lines
                while line:
                    line = self.next_line()
                # tweet starts on another tweets line -> impossible
                raise ValueError("To many collums on single line {}".format({
                    'line_number': ln,
                    'total_line_numbers': self.line_number,
                    'cols': len(arr),
                    'line': line,
                    'array': arr,
                    'last_ended_quote': last_ended_quote,
                    #'prev_line': prev_line,
                }))
            
            self.mapper(arr)
            
            line = self.next_line()
        #print(self.annomalies)
        #print(self.tweet_number)
        #print(self.line_number)
        #print("Skipped "+str(len(self.skipped))+" entries")


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
            hashtags = re.findall(r'#(\w+)', words)
            self.tweet_number += 1
        except Exception as e:
            self.skipped += e
            pass
        for tag in hashtags:
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

