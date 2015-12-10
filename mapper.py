#!/usr/bin/env python
import sys
import csv
import re
import unittest

#settings
maximal_errors = 5
only_count = True

#errors
err_to_large = "Tweet data became to large while combining tweets on line {}"
err_file_end = "File end reached while combining tweets"
err_no_id_found = "Could not identify tweet on line {}, tweet is {}"

#constants
end_quoted = re.compile(r'.*,"(""|[^"])*$')

class Reader:
    #init
    line_number = 0
    tweet_number = 0
    skipped = []
    annomalies = []
    
    def run(self):
        header = next(csv.reader([sys.stdin.readline()]))
        hlength = len(header)
        line = sys.stdin.readline()
        while line:
            self.line_number += 1
            line = line.replace('\0', '').replace('\n', '').replace('\r', '')
            ended_quoted = end_quoted.match(line)
            
            arr = next(csv.reader([line], delimiter=",", quotechar='"'))
            
            if len(arr) == 0:
                self.annomalies += ('newline before tweet', self.line_number)
                arr = [""]
            
            while len(arr) < hlength:  # tweet is acros multiple lines
                line = sys.stdin.readline()
                if not line: raise ValueError(err_file_end)
                self.line_number += 1
                line = line.replace('\0', '').replace('\n', '').replace('\r', '')
                if ended_quoted:
                    line = '"' + line
                else:
                    self.annomalies += (r'text \\n, noquote', self.line_number)
                
                nxt = next(csv.reader([line], delimiter=",", quotechar='"'))
                if len(nxt) == 0:
                    #found an empty line
                    self.annomalies += (r'text \\n, only \\n', self.line_number)
                else:
                    arr[-1] += nxt[0]  # append last entry with first of the new line
                    arr += nxt[1:]  # append the rest
            
            if len(arr) > hlength:  # tweet starts on another tweets line
                raise ValueError("To many collums on 1 line")
            
            self.mapper(arr)
            #TODO check if the last entry ended quoted or unquoted
            # y,"(not " but "" is allowed)  test," test2,"a
            #  test3,""" fail4,"a"a" test5,"a""a
            # y,(not " and not ,)  test, test2,a fail3,a"
            # tweet is split in multiple lines
            # read the next line and try to combine it back into 1 tweet
            line = sys.stdin.readline()
        print(self.annomalies)
        print(self.tweet_number)
        print(self.line_number)


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
    
    def test_regex(self):
        def do_test(string, exp):
            result = end_quoted.match(string)
            if result:
                self.assertEqual(True, exp)
            else:
                self.assertEqual(False, exp)
        do_test('x,"', True)
        do_test('x,"y', True)
        do_test('x,"""', True)
        do_test('x,"y"y"', False)
        do_test('x,"y""y"', False)
        do_test('x","', True)
        do_test('x","y', True)
        do_test('x","""', True)
        do_test('"x","', True)
        do_test('"x","y', True)
        do_test('"x","""', True)
        do_test('"w","x","""', True)
        do_test('"w","x","""', True)
        do_test('"w","x","""', True)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv.pop(1)=="test":
        unittest.main()
    else:
        Reader().run()
