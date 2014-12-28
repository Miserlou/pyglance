#! /usr/bin/env python

# Python port of Glance. Rich Jones 2014.
# Parts of this were inspired by https://github.com/littleq0903/spritz-cmd

from __future__ import print_function
import argparse
import sys
import time

def choose_pivot(word):

    word_length = len(word)
    
    if word_length == 1:
        return 1
    if word_length in [2,3,4,5]:
        return 2
    if word_length in [6,7,8,9]:
        return 3
    if word_length in [10,11,12,13]:
        return 4

    return 4

def get_sleep_interval(wpm):
        time_per_word = 60.0 / wpm
        return time_per_word 

def output(word, pivot):
    start = '\r' + ' '*((4-pivot)) + word[0:pivot-1]
    mid = '\033[31m' + word[pivot-1:pivot] + "\033[0m"
    end = word[pivot:] + ' '*(10-(len(word)-pivot))
    
    out = start + mid + end
    print(out, end='')

def glance(text, wpm=800):
    words = text.split(' ')
    default_sleep_interval = get_sleep_interval(wpm)
    
    for word in words:
        sleep_interval = default_sleep_interval 
        space = False

        two_chars = [',', ':', '-', '(']
        if True in [char in word for char in two_chars] or len(word) > 8:
            sleep_interval = sleep_interval + default_sleep_interval

        spacers = ['.', '!', ':', ';', ')']
        if True in [char in word for char in spacers]:
            space_sleep_interval = (3 * default_sleep_interval)
            space = True

        sys.stdout.flush()
        pivot = choose_pivot(word)
        output(word, pivot)
        time.sleep(sleep_interval)

        if space:
            sys.stdout.flush()
            print('\r                ', end='')
            time.sleep(space_sleep_interval)
    
    print('')

def get_parser():
    parser = argparse.ArgumentParser(description='Glance speed reading for the command line')
    parser.add_argument('file', metavar='FILE', type=str, nargs='*',
                        help='Path to file to glance.')
    parser.add_argument('-s','--speed', help='Speed in Words Per Minute. Default 600.', default=600, type=int)
    return parser

def command_line_runner():
    parser = get_parser()
    smargs = vars(parser.parse_args())

    if not smargs['file']:
        parser.print_help()
        return

    all_content = ''
    for filepath in smargs['file']:
        with open(filepath) as f:
            content = f.readlines()[0].strip()
        all_content = all_content + content

    glance(all_content, smargs['speed'])

if __name__ == '__main__':
    try:
        command_line_runner()
    except Exception, e:
        quit()
