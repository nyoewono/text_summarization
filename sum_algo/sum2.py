#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 20:41:18 2020

@author: nathanaelyoewono
"""

import numpy as np

# for text preprocessing
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.stem.snowball import SnowballStemmer

# import counter
from collections import Counter

class SumTextTwo:
    
    def __init__(self, text):
        self.text = text
    
    def _preprocessing(self):
        
         # convert par into sentences
        self.text = sent_tokenize(self.text)
        
        # lowercase all words (only first letter)
        self.clean_text = self.text.copy()
        func = lambda s: s[:1].lower() + s[1:] if s else ''
        self.clean_text = list(map(func, self.clean_text))
     
        # tokenize each word in the sentence
        stop_words = set(stopwords.words('english'))
        self.clean_text = [word_tokenize(sent) for sent in self.clean_text]
        self.clean_text = self._exclude_stopwords(self.clean_text, stop_words)
        
        # stem each words
        self.clean_text = self._stem_words(self.clean_text)
    
    def _count_freq(self):
        all_words = [j for i in self.clean_text for j in i]
        
        # get all unique words with their corresponding index
        set_corpus = list(set(all_words))
        self.corpus_dic = {set_corpus[i]:i for i in range(len(set_corpus))}
        
        # get each word with their frequency
        corpus = Counter(all_words)
        
        # apply frequency weight
        self.weight_corpus = {i: corpus[i] for i in corpus}
        #print(self.weight_corpus)
    
    def _weight_sent(self, k=5):
        self.matrix = np.zeros((len(self.clean_text), len(self.corpus_dic)))
        self._tf()
        self._idf()
        self._cosine()
        self._agg_cosine(k)
        self._print_sum_text(self.res_sent)
        
        #print(self.dic_res)
        
    def _tf(self):
        
        # calculate the term frequency in the document
        for sent in range(len(self.clean_text)):
            for word in range(len(self.clean_text[sent])):
                word_text = self.clean_text[sent][word]
                self.matrix[sent][self.corpus_dic[word_text]] += 1
            
            self.matrix[sent] = (self.matrix[sent]/len(self.clean_text))
        
    def _idf(self):
        
        self.idf = {}
        tot_sent = len(self.clean_text)
        
        # calculate the idf of each word
        for word in self.weight_corpus:
            count = 0
            for sent in self.clean_text:
                if word in sent:
                    count += 1
                    
            if count!=0:
                self.idf[word] = np.log(tot_sent/count)
            else:
                self.idf[word] = 0
        
        # apply idf in each word
        for word in self.weight_corpus:
            self.matrix[:, self.corpus_dic[word]] *= self.idf[word]
        
    
    def _cosine(self):
        self.sim_matrix = np.zeros((len(self.clean_text), len(self.clean_text)), dtype='float')
        for sent_a in range(len(self.matrix)):
            for sent_b in range(len(self.matrix)):
                self.sim_matrix[sent_a, sent_b] = self._sim(self.matrix[sent_a], self.matrix[sent_b])
    
    def _sim(self, a, b):
        num = np.sum(a*b)
        denom = np.sqrt(np.sum(a**2))*np.sqrt(np.sum(b**2))
        if denom==0:
            return 0
        else:
            return num/denom
    
    def _agg_cosine(self, k):
        self.dic_res = {}
        for sent in range(len(self.sim_matrix)):
            self.dic_res[sent] = np.mean(self.sim_matrix[sent])
        
        # sort the dictionary
        self.dic_res = dict(sorted(self.dic_res.items(), key=lambda item: item[1]))
        #print(self.dic_res)
        self.res_sent = list(self.dic_res.keys())[-k:]
            
    def summarize(self, k=5):
        self._preprocessing()
        self._count_freq()
        self._weight_sent(k)
    
    def _print_sum_text(self, sent):
        for each_sent in sent:
            print(self.text[each_sent], end=' ')
        print('\n')
        
    def _exclude_stopwords(self, sent, stop_words):
        """Used to exclude stopwords and number contained in the sentence"""
        clean_sent = []
        
        # set translator to translate all punc to None
        punc = '!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~'
        translator = str.maketrans('', '', punc)
        
        # iterate for each sentence
        for each_sent in sent:
            words = []
            for word in each_sent:
                if word not in stop_words and word.isdigit()==False:
                    word = word.translate(translator)
                    if word!='':
                        words.append(word)
            clean_sent.append(words)
        return clean_sent
    
    def _stem_words(self, lst_sent):
       """Helper function to find the origin of each words"""
       
       # find each words' root 
       stemmer = SnowballStemmer("english")
       
       # iterate for each sentence and words
       for ind_sent in range(len(lst_sent)):
           for ind_word in range(len(lst_sent[ind_sent])):
               lst_sent[ind_sent][ind_word] = stemmer.stem(lst_sent[ind_sent][ind_word])
       
       return lst_sent

#sample = 'From the formula above, it is clear that if a phrase only occurs in a few documents, denominator will be small and this will result in higher value of IDF. Similarly, if phrase occurs in many documents, denominator will be big and hence IDF value will be smaller. TF-IDF is the product of TF & IDF values. For a phrase to have higher TF-IDF score, it should appear often in a document and be absent in other documents of the corpus.A phrase having high value of TF-IDF would imply word is of more importance.'
#summarizer = SumTextTwo(sample)
#summarizer.summarize()
    
    
        