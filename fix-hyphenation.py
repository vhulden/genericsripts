# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 18:42:43 2015

@author: Vilja Hulden

A script for fixing hyphenation problems often left by OCR, i.e., this kind of
stuff:

There once was a litt-
le boy who did not really much care for his grandmo- ther.

The basic idea is to split the text into a list of words and for each word
check if it ends in '-'; if it does, combine it with next word. Then check
if the spellchecker approves the next word. If not, scratch that, and instead
add the word without the "-" at the end.
"""

import os,re
from enchant.checker import SpellChecker
chkr = SpellChecker("en_US")
# Change workdir and filedir to suit your needs.
# filedir is where the full-text versions of the articles reside.
workdir = ""
filedir = "hyphproblem/"
writedir = "hyphcorrected/"
if not os.path.exists(writedir):
    os.makedirs(writedir)


files = os.walk(workdir+filedir)

for fn in files:
    filenames = fn[2]

flag = 0
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
        elif flag: #this is to control that we address the correct words in each iteration
            flag = 0
            i += 1
            continue
        else:    
            newwordslist.append(word)
        i += 1
    newtext = " ".join(newwordslist)
    with open(workdir+writedir+filename, 'w') as f:
        f.write(newtext)

    
    
