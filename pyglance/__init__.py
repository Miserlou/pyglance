#! /usr/bin/env python

# Python port of Glance. Rich Jones 2014.
# Parts of this were inspired by https://github.com/littleq0903/spritz-cmd

from __future__ import print_function
import argparse
import requests 
import sys
import time
import urllib

# Really shouldn't do this.
DIFFBOT_API_TOKEN = '2efef432c72b5a923408e04353c39a7c'

def get_page_data(url):
    diffbot_url = 'http://api.diffbot.com/v2/article?url=' + urllib.quote_plus(url) + "&token=" + DIFFBOT_API_TOKEN
    page = requests.get(diffbot_url)
    data = page.json()

    if 'error' in data:
        print(data['error'])
        quit()

    return data

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

def output(word, pivot, width=0):
    start = '\r' + ' '*((4-pivot)) + word[0:pivot-1]
    mid = '\033[31m' + word[pivot-1:pivot] + "\033[0m"
    end = word[pivot:] + ' '*(10-(len(word)-pivot))
    
    out = start + mid + end
    print(out + (width-len(out))*' ', end='')

def glance(text, wpm=800):
   
    (width, height) = get_terminal_size()
 
    # Remove special chars
    text = text.replace('\n', '')
    text = text.replace('\r', '')
    text = text.replace('\t', '')

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
        output(word, pivot, width)
        time.sleep(sleep_interval)

        if space:
            sys.stdout.flush()
            #print('\r                ', end='')
            print('\r' + ' '*width, end='')
            time.sleep(space_sleep_interval)
    
    print('')

# Stolen from: http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python
# Not sure if this is windows compatible. 
def get_terminal_size():
    import os
    env = os.environ
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
        '1234'))
        except:
            return
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))

        ### Use get(key[, default]) instead of a try/catch
        #try:
        #    cr = (env['LINES'], env['COLUMNS'])
        #except:
        #    cr = (25, 80)
    return int(cr[1]), int(cr[0])

def read_file_contents(path):
    all_content = ''
    for filepath in path:
        with open(filepath) as f:
            content = f.read().strip()
        all_content = all_content + content
    return all_content

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

    inpath = smargs['file']
    all_content = ''

    if 'http:' in inpath[0] or 'https:' in inpath[0]:
        all_content = get_page_data(inpath[0]) 
        all_content = all_content['text']
    else:
        all_content = read_file_contents(inpath)
    
    glance(all_content, smargs['speed'])

def runner():
    try:
        command_line_runner()
    except (KeyboardInterrupt, SystemExit):
        print()
        quit()
    except Exception, e:
        quit()

if __name__ == '__main__':
    try:
        command_line_runner()
    except (KeyboardInterrupt, SystemExit):
        print()
        quit()
    except Exception, e:
        print(e)
        quit()
