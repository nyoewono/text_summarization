#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 16:59:38 2020

@author: nathanaelyoewono
"""

#from sum1 import SumTextOne
#from sum2 import SumTextTwo
from summ import SumTextOne, SumTextTwo
from scrape_wikipedia import Scrape

article = input('Set the wikipedia article you want to summarise: ')
threshold = float(input('Input threshold for summarize: '))
k = int(input('Input k for summarize: '))

# scrape the article in wikipedia
scraper = Scrape(article)
article = scraper._fetch_article()

# summarize the article
summarizer_one = SumTextOne(article)
summarizer_one.summarize(threshold)

summarizer_two = SumTextTwo(article)
summarizer_two.summarize(k)