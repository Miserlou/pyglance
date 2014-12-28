# pyglance

A python client and library for [Glance](http://github.com/Miserlou/Glance) applications. 

It's not the best because it doesn't have top/bottom registration marks yet. Improvements welcome.

## Installation

    pip install pyglance -g

## Usage (CLI)

    $ glance filename.txt
    $ glance file1.txt file2.txt --speed 500

## Usage (Programmatic)

    from pyglance import glance
    
    glance(your_text_string)
    wpm = 800
    glance(your_text_string, wpm)

## About

There were some other attempts to do this, but none that quite accurately matched the 'Glance' timing and spacing specification.

This is used by the [seek](http://github.com/Miserlou/seek) project.

3 Clause BSD, Rich Jones 2014.
