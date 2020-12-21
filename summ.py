#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 23:32:55 2020

@author: nathanaelyoewono
"""

import numpy as np

# for text preprocessing
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.stem.snowball import SnowballStemmer
import re

# import counter
from collections import Counter

class Summarize:
    
    def __init__(self, text):
        self.text = text
    
    def _preprocessing(self):
        """Prepare the sentences for tf-idf and cosine similarity"""
        
        # convert par into sentences
        self.text = sent_tokenize(self.text)
        
        # lowercase all words
        self.clean_text = self.text.copy()
        self.clean_text = [sent.lower() for sent in self.clean_text]
        
        # tokenize each word in the sentence
        stop_words = set(stopwords.words('english'))
        self.clean_text = [word_tokenize(sent) for sent in self.clean_text]
        self.clean_text = self._exclude_stopwords(self.clean_text, stop_words)
        
        # stem each words
        self.clean_text = self._stem_words(self.clean_text)
    
    def _print_sum_text(self, sent):
       for each_sent in sent:
           print_sent = re.sub(r'[[]\d+]', '', self.text[each_sent-1])
           print(print_sent, end=' ')
       print('\n')
    
    def _stem_words(self, lst_sent):
        """Helper function to find the origin of each words"""
        
        # find each words' root 
        stemmer = SnowballStemmer("english")
        
        # iterate for each sentence and words
        for ind_sent in range(len(lst_sent)):
            for ind_word in range(len(lst_sent[ind_sent])):
                lst_sent[ind_sent][ind_word] = stemmer.stem(lst_sent[ind_sent][ind_word])
        
        return lst_sent
        
        
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
    
class SumTextOne(Summarize):
    
    """
    The class was made to summarize any given text using extraction method.
    Algorithm inspired by: https://blog.floydhub.com/gentle-introduction-to-text-summarization-in-machine-learning/
    """
    
    def _count_freq(self, text):
        all_words = [j for i in text for j in i]
        corpus = Counter(all_words)
        
        # apply frequency weight
        self.weight_corpus = {i: corpus[i] for i in corpus}
        
    def _apply_weight(self):
        """Apply the weight for each words"""
        self.dic_sent_weight = {}
        for each_sent in range(len(self.clean_text)):
            for each_word in range(len(self.clean_text[each_sent])):
                self.clean_text[each_sent][each_word] = self.weight_corpus[self.clean_text[each_sent][each_word]]
            try:
                self.dic_sent_weight[each_sent+1] = sum(self.clean_text[each_sent])/len(self.clean_text[each_sent])
            except:
                pass
                        
        #print(self.dic_sent_weight)
    
    def _take_imp_sent(self, par_threshold=1):
        # set threshold sent score as the average
        threshold = np.mean(list(self.dic_sent_weight.values()))*par_threshold
        imp_sent = [i for i in self.dic_sent_weight if self.dic_sent_weight[i]>threshold]
        return imp_sent
    
    def _stem_words(self, lst_sent):
        """Helper function to find the origin of each words"""
        
        # find each words' root 
        stemmer = SnowballStemmer("english")
        
        # iterate for each sentence and words
        for ind_sent in range(len(lst_sent)):
            for ind_word in range(len(lst_sent[ind_sent])):
                lst_sent[ind_sent][ind_word] = stemmer.stem(lst_sent[ind_sent][ind_word])
        
        return lst_sent
    
    def summarize(self, par_threshold):
        Summarize._preprocessing(self)
        self._count_freq(self.clean_text)
        self._apply_weight()
        sent = self._take_imp_sent(par_threshold)
        Summarize._print_sum_text(self, sent)

class SumTextTwo(Summarize):
    
    """
    The class was made to summarize any given text using extraction method.
    Algorithm inspired by: https://medium.com/datapy-ai/nlp-building-text-summarizer-part-1-902fec337b81
    """
    
    def _count_freq(self):
        all_words = [j for i in self.clean_text for j in i]
        
        # get all unique words with their corresponding index
        set_corpus = list(set(all_words))
        self.corpus_dic = {set_corpus[i]:i for i in range(len(set_corpus))}
        
        # get each word with their frequency
        corpus = Counter(all_words)
        
        # apply frequency weight
        self.weight_corpus = {i: corpus[i] for i in corpus}
    
    def _weight_sent(self, k=5):
        self.matrix = np.zeros((len(self.clean_text), len(self.corpus_dic)))
        self._tf()
        self._idf()
        self._cosine()
        self._agg_cosine(k)
        Summarize._print_sum_text(self, self.res_sent)
        
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
        self.res_sent = list(self.dic_res.keys())[-k-1:]
        self.res_sent = sorted(self.res_sent)
            
    def summarize(self, k=5):
        Summarize._preprocessing(self)
        self._count_freq()
        self._weight_sent(k)
    
    