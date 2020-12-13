#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 16:58:37 2020

@author: nathanaelyoewono
"""

import bs4
import requests

class Scrape:
    
    def __init__(self, article):
        self.article = article
    
    def _fetch_article(self):
        response = requests.get('https://en.wikipedia.org/wiki/'+self.article)
        print('\n')
        article = ''
        if response is not None:
            html = bs4.BeautifulSoup(response.text, 'html.parser')
            pars = html.select("p")
            for par in pars:
                article += par.text
        return article


