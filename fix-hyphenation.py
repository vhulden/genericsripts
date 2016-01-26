# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 18:42:43 2015

@author: Vilja Hulden

A script for converting a JSTOR data for research citations file (.csv) into a BibTex file (.bib) for importation into Zotero (or to any reference manager that understands BibTex, for that matter).

If you do not wish to include the links to the actual files in the Zotero format, set includefiles below to 0.

This script assumes .txt files named as they come from JSTOR Data for Research.
"""

import os,re
from enchant.checker import SpellChecker
chkr = SpellChecker("en_US")
# Change workdir and filedir to suit your needs.
# filedir is where the full-text versions of the articles reside.
workdir = "/Users/miki/work/research/digital/JSTOR-laborlaw/"
filedir = "renamedbyyear/"
writedir = "hyphcorrected/"

tempfile = "/Users/miki/work/research/digital/JSTOR-laborlaw/renamedbyyear/1946_ocr_10.2307_1896734.txt"

files = os.walk(workdir+filedir)

for fn in files:
    filenames = fn[2]


for filename in filenames:
    with open(workdir+filedir+filename) as f:
        text = f.read()
        words = text.split()
        
    
    newwordslist = []
    i = 0
    for word in words:
        if re.search('[a-zA-Z]',word,flags=0) and word.endswith('-') and i<len(words)-1:
            newword = word[:-1] + words[i+1]
           # print word
            #print newword
            newwordstripped = re.search('\s*[a-zA-Z0-9]+',newword,flags=0).group(0)
            if chkr.check(newwordstripped):
                newwordslist.append(newword)
                flag = 1
            else:
                newwordslist.append(word[:-1])
        elif flag:
            flag = 0
            i += 1
            continue
        else:    
            newwordslist.append(word)
        i += 1
    newtext = " ".join(newwordslist)
    with open(workdir+writedir+filename, 'w') as f:
        f.write(newtext)

   
"""with open(workdir+readfile) as f:
    entriestemp = f.read()
    entries = [line for line in entriestemp.split('\n') if line.strip() != '']



with open(workdir+writefile, 'w') as f:
    f.write(bibentriestext)"""
    
    
