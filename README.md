# pyglance

A python client and library for [Glance](http://github.com/Miserlou/Glance) applications. 

It's not the best because it doesn't have top/bottom registration marks yet. Improvements welcome.

## Installation

    pip install pyglance -g

## Usage (CLI)

    glance filename.txt

## Usage (Programmatic)

    from pyglance import glance
    
    glance(your_text_string)
    glance(your_text_string, wpm=800)

## About

There were some other attempts to do this, but none that quite accurately matched the 'Glance' timing and spacing specification.

This is used by the [seek](http://github.com/Miserlou/seek) project.
