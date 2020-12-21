#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 11:59:46 2020

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

class SumTextOne:
    
    """
    The class was made to summarize any given text using extraction method.
    Algorithm inspired by: https://blog.floydhub.com/gentle-introduction-to-text-summarization-in-machine-learning/
    """
    
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
    
    def _count_freq(self, text):
        all_words = [j for i in text for j in i]
        corpus = Counter(all_words)
        #max_freq = max(corpus.values())
        
        # apply frequency weight
        self.weight_corpus = {i: corpus[i] for i in corpus}
        #print(self.weight_corpus)
        
    
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
    
    def _print_sum_text(self, sent):
        for each_sent in sent:
            print(self.text[each_sent-1], end=' ')
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
    
    def summarize(self, par_threshold):
        self._preprocessing()
        self._count_freq(self.clean_text)
        self._apply_weight()
        sent = self._take_imp_sent(par_threshold)
        self._print_sum_text(sent)
    
     