#!/usr/bin/env python
import sys
import csv
import re

#settings
maximal_errors = 5
only_count = True

#errors
err_to_large = "Tweet data became to large while combining tweets on line {}"
err_file_end = "File end reached while combining tweets"
err_no_id_found = "Could not identify tweet on line {}, tweet is {}"

#constants
end_quoted = re.compile(r'.*,"(""|[^"])*$')

def mapper():
    #init
    errors = []
    line_number = 0
    tweet_number = 0
    header = next(csv.reader([sys.stdin.readline()]))
    hlength = len(header)
    print("Header found (size="+str(len(header))+")")
    
    exit()
    line = sys.stdin.readline()
    while line:
        line_number += 1
        line = line.replace('\0', '').replace('\n', '').replace('\r', '')
        arr = next(csv.reader([line], delimiter=",", quotechar='"'))
        while len(arr) < hlength:
            #TODO check if the last entry ended quoted or unquoted
            # y,"(not " but "" is allowed)  test," test2,"a test3,""" fail4,"a"a" test5,"a""a
            # y,(not " and not ,)  test, test2,a fail3,a"
            if end_quoted.match(line):
                print(['found match', line])
                line = '"' + line
                
            # tweet is split in multiple lines
            # read the next line and try to combine it back into 1 tweet        
            line = sys.stdin.readline()
            if not line: raise ValueError(err_file_end)
            line_number += 1
            line = line.replace('\0', '').replace('\n', '').replace('\r', '')
            
            nxt = next(csv.reader([line], delimiter=",", quotechar='"'))
            if len(nxt) > 0:
                arr[-1] += nxt[0]  # append last entry with first of the new line
                arr += nxt[1:]  # append the rest
        try:
            float(arr[0])
        except ValueError:
             raise ValueError(err_no_id_found.format(line_number, arr))
        if len(arr) > hlength:
            print({
                'line': line,
                'arr': arr,
                'arr length': len(arr),
            })
            raise ValueError(err_to_large.format(line_number))
        
        
        tweet_number += 1
        line = sys.stdin.readline()
    print("OK "+str(line_number)+" lines to "+str(tweet_number)+" tweets")
    exit()
        #get the full tweet
        #arr = next(csv.reader([line], delimiter=",", quotechar='"'))
        #while len(arr) < header_size:
        #    line = sys.stdin.readline()
            
    while False:
        line = line.replace('\0', '').replace('\n', '').replace('\r', '')
        arr = next(csv.reader([line], delimiter=",", quotechar='"'))
        
        line_number += 1
        
        try:
            words = arr[4].strip()
            date = arr[5].strip()
            date = date[:-9]
            hashtags = re.findall(r'#(\w+)', words)
            for tag in hashtags:
                print tag, 1
        except Exception as e:
            print("Error at line "+str(line_number)+": "+str(e))
            errors.append(e)
            if len(errors) >= maximal_errors:
                raise errors[0]
        
        line = sys.stdin.readline()

    print("Success, lines: "+str(line_number))

def test_regex():
    def do_test(string, outcome):
        if end_quoted.match(line) is not outcome:
            raise AssertionError("test failed on << "+str(string)+" >>")
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

if __name__ is '__main__':
    mapper()

