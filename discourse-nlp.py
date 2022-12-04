import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import heapq
import csv
import datetime
# ntlk type beats
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from vader import *
from _utils import print_full, scrolling

'''
Discourse scraper and sentiment analysis tool. Can be used
for majority of boards using the service. Reach out if you find a particular site isn't pulling!

Otherwise, enjoy! :)

'''

MAP = {

    'MakerDAO': 'https://forum.makerdao.com/top?period=yearly',
    'Aave': 'https://governance.aave.com/top?period=yearly',
    'Uniswap': 'https://gov.uniswap.org/top?period=yearly',

}

for doc in MAP.keys():
    url = MAP[doc]
    protocol = url.split('.')[1]  # grabs site name from href

    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')

    links = []
    top_line = [a['href']
                for a in soup.findAll('a', class_='title') if a.stripped_strings]  # first page post links

    for line in top_line:
        links.append(line)

    for link in links:
        # for l in link:
        res = requests.get(link).text
        souped = BeautifulSoup(res, 'html.parser')

        for content in souped.findAll('div', itemprop='articleBody'):
            article = content.text
            # strip brackets and extra space
            article_text = re.sub(r'\[[0-9]*\]', ' ', article)
            article_text = re.sub(r'\s+', ' ', article_text)
            # strip special chars and digits
            formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text)
            formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

            sentence_list = nltk.sent_tokenize(article_text)

            # weighted frequency
            stopwords = nltk.corpus.stopwords.words('english')

            word_frequencies = {}
            for word in nltk.word_tokenize(formatted_article_text):
                if word not in stopwords:
                    if word not in word_frequencies.keys():
                        word_frequencies[word] = 1
                    else:
                        word_frequencies[word] += 1

            for word in word_frequencies.keys():
                maximum_frequncy = max(word_frequencies.values())
                word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
            # tokenized word list and frequency scores
            df = pd.DataFrame({
                'word': word_frequencies.keys(),
                'frequency scores': word_frequencies.values()
            })
            # tokenized word list
            word_list = pd.DataFrame({
                'word': word_frequencies.keys()
            })
            # tokenized sentence list
            sent_list = pd.DataFrame(
                {'sentence': [sentence_list], 'protocol': protocol})

            current_date = f'defi_nlp{datetime.datetime.now().strftime("%m.%d.%Y")}.csv'

            print_full(word_list.head())

            # word_list.to_csv(current_date, mode='a', header=None)
