import os, os.path, re

rootDir = '.' # look down from this directory
outputFile = 'strings.csv' # output table of strings to this file
pattern1 = "(?P<quote>['\"`])(?P<words>.*?)(?P=quote)"
pattern2 = "(?m)<(?P<tag>[A-Za-z\-]+).*?>(?P<innerHTML>.*?)<\/(?P=tag)>"
pattern3 = "@{4}.*?\?>"
pattern4 = "@{4}[^(?>)]*"
inString = re.compile(pattern1)
inTags = re.compile(pattern2, re.DOTALL)
inPhp = re.compile(pattern3, re.DOTALL)
phpNoEnd = re.compile(pattern4, re.DOTALL)
StringArray = [] # format: filename, line, NinLine, string

def CheckContent(fname, st):
    #print st
    if len(st) < 1:
        return True
    global inTags
    res = True
    nFound = 0
    for cont in inTags.finditer(st):
        nFound += 1
        if not (CheckContent(fname, cont.group("innerHTML"))):
            print '"' + fname + '";;;"' + cont.group("innerHTML").replace('"','""') + '"'
    if nFound == 0:
        res = False
    return res

def CheckTheFile(fname):
    global inPhp
    f = open(fname)
    Content = f.read()
    f.close()
    c = Content.replace("<?php", "@@@@")
    if phpNoEnd.match(c):
        return
    Comtent = inPhp.sub('',c)
    #print Content
    #print '\n\n*********************************' + fname + '********************************\n\n'
    if not(CheckContent(fname, Comtent)):
        print '"' + fname + '";;;"' + Comtent.replace('"','""') + '"'

for root, dirs, files in os.walk(rootDir):
    for fname in files:
        if os.path.splitext(fname)[1] in ['.php']:
            CheckTheFile(os.path.join(root,fname))

#print pattern
