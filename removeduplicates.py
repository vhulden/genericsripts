# -*- coding: utf-8 -*-
"""
Created on Sun Nov 16 07:42:06 2014
Modified Jan 2016
@author: Vilja
"""
"""
This takes in a list of e.g. names or places, sorts it, and tries to 
...remove duplicates using fuzzy matching. The application is e.g. for 
...culling lists of names or companies from various OCR'd sources and wanting
...a complete list without duplicates and with the most accurate version
...of each repeated name/company etc.

The idea is to keep either the longer line (with more information), or, 
...if about equal length, the one where spelling is more accurate 
...(not so many OCR errors).
  
So the input is:
Name1
Name2
Name3
...

Alternatively, if readsecondfile is defined, compare one list to another. In
...this case, we presume we have two lists with lots of duplicates and we want
...to know which ones are in one list but not the other (in readfile but not in
...readsecondfile.)

"""

from enchant.checker import SpellChecker
import Levenshtein
import re


chkr = SpellChecker("en_US")
mydir = "/Users/vilja/work/digitalresearch/employerorglists/"

#writedir = "/Users/miki/work/"

#readfile = "testfile1.csv"
#readsecondfile = "testfile2.csv"
readfile = "companies_1906_namesonlywithother.csv"
#readsecondfile = ""
readsecondfile = "companies_1913_namesonlywithother.csv"
outputfile = "uniques.txt"
outputfile2 = "matches.txt"
mylist = []

with open(mydir+readfile) as f:
    firstfile = f.read()

   
firstfilelines = sorted(firstfile.splitlines(),key=lambda v: v.upper())

#firstfilelinessave = sorted(myfile.splitlines())



if readsecondfile:
    possibleuniques = []
    probablematches = []
    with open(mydir+readsecondfile) as f:
        secondfile = f.read()
    secondfilelines = sorted(secondfile.splitlines(),key=lambda v: v.upper()) 
    for line in firstfilelines:
        candidate1 = line.strip().lower()
        candidate1 = re.sub('company','',candidate1)
        candidate1 = re.sub('american','',candidate1)
        #probablematch = ""
        for idx, cline in enumerate(secondfilelines):
            candidate2 = cline.lower()
            candidate2 = re.sub('company','',candidate2)
            candidate2 = re.sub('american','',candidate2)
            candidate2 = candidate2.strip()
            if Levenshtein.distance(candidate1[:20],candidate2[:20]) < 4:
                probablematch = line + " # " +cline #i.e., original versions of candidate1 adn candidate2
                probablematches.append(probablematch)
                break
        else:
            possibleunique = line
            possibleuniques.append(possibleunique)
    probablematchestxt = '\n'.join(probablematches)
    possibleuniquetxt = '\n'.join(possibleuniques)
    with open(mydir+outputfile,'w') as f:
        f.write(possibleuniquetxt)
    with open(mydir+outputfile2,'w') as f:
        f.write(probablematchestxt)
                     
else:
    
    repeat = 1
    while repeat > 0: #that is, we do this as long as we keep finding candidates within the set Levenshtein distance
        repeat = 0
        for index, line in enumerate(firstfilelines):
            #print line
        #    while index < len(firstfilelines):
            if index < len(firstfilelines)-1:
                candidate1 = line.strip().lower()
                candidate2 = firstfilelines[index+1].strip().lower()
     #           if candidate1.startswith('Eve'): print 'C1:' + candidate1
      #          if candidate2.startswith('Eve'): print 'C2:' + candidate2
                if Levenshtein.distance(candidate1[:20],candidate2[:20]) < 7:
                    repeat += 1
                    errone = []
                    errtwo = []
                    if abs(len(candidate1)-len(candidate2)) < 10: #only if about same length
                        chkr.set_text(line)
                        for err in chkr: 
                                errone.append(err.word)
                        chkr.set_text(firstfilelines[index+1])
                        for err in chkr:
                            errtwo.append(err.word)
                        if len(errone) > len(errtwo):
                            firstfilelines.pop(index)
                        else:
                            firstfilelines.pop(index+1)
                    else:
                        if len(candidate1) > len(candidate2): #delete shorter
                            firstfilelines.pop(index+1)
                        else:
                            firstfilelines.pop(index)
    mylist = '\n'.join(firstfilelines)
    
    with open(mydir+outputfile,'w') as f:
        f.write(mylist)
