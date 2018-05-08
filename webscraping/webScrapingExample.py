''' Reversing a string in many ways :)
test = 'hello'
for i in range(-1, -len(test)-1, -1):
    print(test[i])

reverseTest = test[::-1]

print(reverseTest)
'''


## all imports## all  
#from IPython.display import HTML
import numpy as np
#import urllib2
import bs4 #this is beautiful soup

import matplotlib
import matplotlib.pyplot as plt

import seaborn as sns
sns.set_context("talk")
sns.set_style("white")

import requests #Helps construct the request to send to API
import json #JSON helper functions
from bs4 import BeautifulSoup   #Data Scraping library
import pandas as pd
import time

'''
Parsing the Tree example
'''
# redifining `s` without any line breaks
s = """<!DOCTYPE html><html><head><title>This is a title</title></head><body><h3> Test </h3><p>Hello world!</p></body></html>"""
## get bs4 object
tree = bs4.BeautifulSoup(s, "html5lib")

## get html root node
root_node = tree.html

## get head from root using contents
head = root_node.contents[0]

## get body from root
body = root_node.contents[1]

## could directly access body
treeBody = tree.body

'''
Parsing beautfulsoup site (https://www.crummy.com/software/BeautifulSoup/)
'''
url = 'http://www.crummy.com/software/BeautifulSoup'
response = requests.post(url)
soup = BeautifulSoup(response.text, "html5lib")
## get all links in the page and length of linkList = 40
linkList = [l.get('href') for l in soup.findAll('a')]
externalLinks = []
#if it is not None and starts with 'http' we are happy. ExternalLinks = 24
for l in linkList:
    if l is not None and l[:4] == 'http':
        externalLinks.append(l)
#alternative to the if statement
#[l for l in linkList if l is not None and l.startswith()]

'''
Parsing beatifulsoup site for Hall Of Fame
'''
soupUrl = 'http://www.crummy.com/software/BeautifulSoup'
soupResponse = requests.post(soupUrl)
b = BeautifulSoup(soupResponse.text, "html5lib")
#use ul as entry point
entryPoint = b.find('ul')
hallOfFameList = entryPoint.contents[1:]
tmp = []
for li in hallOfFameList:
    tmp.append(li.contents)

test = ["".join(str(a) for a in sublist) for sublist in tmp]
# print('\n'.join(test))

'''
Python Dictionaries
- uses key: value pairs
'''
a = {'a': 1, 'b': 2}
# show keys
a.keys()
# show values
a.values()
# option 1
'''
# show for loop over all entries
for k,v in zip(a.keys(), a.values()):
    print(k,v)
'''
# option 2
'''
# option 2 using the dictionary iteritems() function
for k,v in a.iteritems():
    print(k,v)
'''

'''
JSON
'''
a = {'a': 1, 'b':2}
s = json.dumps(a)
a2 = json.loads(s)

## a is a dictionary
#a
## vs s is a string containing a in JSON encoding
#s
## reading back t

