#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: vilja

Read in all files in one directory.
Add a year - or any sequential number - as the first line of 
each data file since that way NLP4DH determines the sequence
that can be used in drawing graphs. 
Write the files in another directory.
Note that the year (or whatever sequence) comes from the filename, so
how to get the year depends on the filename format.
This was written for the case where the sequence is a year,
so it assumes that it's always the same length and in the same place 
(in this case, the first 4 characters of the filename.)
"""

import os,codecs

mydir = "NLPproject/FRUS-TXT/"
writedir = "docker/frus/"
if not os.path.isdir(writedir):
    os.mkdir(writedir)

fn = 0
for item in os.listdir(mydir):
    
    fn +=1
    print "Processing file number {0},{1}".format(fn,item)
    if os.path.isfile(mydir+item) :
        with codecs.open(mydir+item,'r',encoding='utf-8') as f:
            thisfile = f.read()
        #below assumes year is first 4 chars. You can change things if need be: 
        #...say you have a two-digit year and it's the last 2 chars, you'd do:
        #...year = item[-2:]
        #...or if it's chars 4,5,6,7, you'd do
        #... year = item[3:7]
        year = item[:4] 
        #if the sequential number you have is of the format 01, 02, .... 11, 12,
        #...the tool will not like the leading zeroes. To get rid of them, 
        #...uncomment the line below.
        #if year[0] == '0': year = year[1:]
        newfile = year + "\n" + thisfile
        with codecs.open(writedir+item,'w',encoding='utf-8') as f:
            f.write(newfile)
        

