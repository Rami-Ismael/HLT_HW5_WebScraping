import urllib
from urllib import request
import urllib.request
import nltk
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

import requests
import selenium
import lxml


def pre_process(text: str):
    print(string.punctuation)

    text = text.lower()
    tokens = word_tokenize(text)
    excludingWords = list(stopwords.words("english"))
    excludingWords.extend(string.punctuation)
    excludingWords.extend(string.whitespace)

    returnTokens = []
    for token in tokens:
        if token not in excludingWords:
            returnTokens.append(token)
    return returnTokens


def frequncy(text_tokens: list[str]):
    freq_dict = dict()
    for token in text_tokens:
        if token in freq_dict.keys():
            freq_dict[token] = freq_dict[token] + 1
        else:
            freq_dict[token] = 1


def getWebpage(URL: str):
    print(string.punctuation)
    html = request.urlopen(URL).read().decode('utf8')
    soup = BeautifulSoup(html, features="html.parser")
    text = soup.get_text()

    # response = requests.get(URL)
    # soup = BeautifulSoup(response.text, features="html.parser")
    # text = soup.get_text()


    print(text[:200])

    import re
    text_chunks = [chunk for chunk in text.splitlines() if not re.match(r'^\s*$', chunk)]
    for i, chunk in enumerate(text_chunks):
        print(i + 1, chunk)


# https://github.com/kjmazidi/NLP/tree/master/Xtra_Python_Material/Web_Scraping
def webCrawler():
    pass


if __name__ == '__main__':
    getWebpage("https://gameofthrones.fandom.com/wiki/Jon_Snow")
