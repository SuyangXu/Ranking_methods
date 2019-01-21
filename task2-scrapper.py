#!/usr/bin/env python
# coding: utf-8

import requests
from bs4 import BeautifulSoup
import pandas as pd
from collections import Counter
from string import punctuation
import re


# get html
url = 'https://en.wikipedia.org/wiki/International_Monetary_Fund'
html = requests.get(url)
soup = BeautifulSoup(html.text, 'lxml')


def Remove(duplicate): 
    final_list = [] 
    for num in duplicate: 
        if num not in final_list: 
            final_list.append(num) 
    return final_list 

# find all tags and prepare to filter invisible ones
tag_list = [tag.parent.name for tag in soup.find_all(text=True)]
Remove(tag_list)

def find_visible(element):
    from bs4.element import Comment
    if element.parent.name in ['[document]', 'html', 'head', 'title','script', 'sup', 'style','sub','noscript', 'meta']:
        return False
    if isinstance(element, Comment):
        return False
    return True

texts = soup.findAll(text=True)
visible_texts = filter(find_visible, texts) 
words = (''.join(re.sub('[^a-zA-Z]+', '', i)) for s in visible_texts for i in s.split())
c = Counter((x.rstrip(punctuation).lower() for y in words for x in y.split()))
df = pd.DataFrame.from_dict(c, orient='index').reset_index().rename(columns={'index':'word', 0:'count'})

df.to_csv('scrapper.csv')