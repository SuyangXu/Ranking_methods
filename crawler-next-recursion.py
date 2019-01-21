#!/usr/bin/env python
# coding: utf-8


##########################################################################################
# Comments
# Because Wikipedia provides a link containing all article links on the term page (IMF here),
# I took advantage of the property and used url_2 as defined below to retrieve all links 
# and title for wikipedia article link on the IMF page.
# 
# Functions:
#   get_soup is a function to call links via requests and get its html as soup
#   get_links is a function to get links and titles from selected soup and store 
#                them into a dataframe.
#   recurse_pages is a function to collect all page links on clicking "next 50" button on
#                    the webpage by recursion. It gives a list of links to call and get
#                     links and article titles.
##########################################################################################


import requests
from bs4 import BeautifulSoup
import pandas as pd
import re



def get_soup(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'lxml')
    return soup


def get_links(some_soup):
    links = some_soup.find('ul', attrs={'id':'mw-whatlinkshere-list'})
    dic_wiki = {}
    for s in links.findAll('a', href = True):
        new_url = s.get('href')
        title = s.get('title')
        if not re.search('php',new_url):
            new_url = 'https://en.wikipedia.org' + new_url
            dic_wiki[new_url] = title     
    df_wiki = pd.DataFrame.from_dict(dic_wiki, orient = 'index', columns = ['title'])
    return df_wiki



def recurse_pages(link, list_page): 
    list_page.append(link)
    soup = get_soup(link)
        
    pages = soup.find('div', attrs = {'id':'mw-content-text'})
    for s in pages.findAll('a', href = True):
        if re.search('next 50', s.text) and 'https://en.wikipedia.org' + s.get('href') not in list_page:
            recurse_pages('https://en.wikipedia.org' + s.get('href'), list_page)
    return list_page



url_2 = 'https://en.wikipedia.org/w/index.php?title=Special%3AWhatLinksHere&target=International+Monetary+Fund&namespace=0'
list_page2 = []
list_ = recurse_pages(url_2, list_page2)

df = pd.DataFrame()
for i in list_:
    curr = get_links(get_soup(i))
    df = pd.concat([df, curr], axis=0)


df.to_csv("crawler.csv", sep='\t', encoding = 'utf-8')


