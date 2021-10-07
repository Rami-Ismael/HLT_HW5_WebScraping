import urllib
from urllib import request
import urllib.request
import nltk
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

import requests
# import selenium
# import lxml


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
    html = request.urlopen(URL).read().decode('utf8')
    soup = BeautifulSoup(html, features="html.parser")
    text = soup.prettify()

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


def getBodyText(URL: str, tokensLength: int = 5, DEBUG: bool = False):
    # response = request.urlopen(URL).read().decode('utf8')
    # soup = BeautifulSoup(response, features="html.parser")
    # text = soup.get_text()

    response = requests.get(URL)
    soup = BeautifulSoup(response.text, features="html.parser")
    text = soup.get_text()

    # tokens = text.splitlines()
    # newToks = [line for line in tokens if len(line.split()) > tokensLength]
    # print(newToks)
    # #print(text)

    tags = soup.body

    bodySents = [str(line).strip() for line in soup.body.strings if len(line.strip().split()) > tokensLength
                 and line.find("©") == -1]

    if DEBUG:
        print(bodySents)


    # import re
    # text_chunks = [chunk for chunk in bodySents if not re.match(r'^\s*$', chunk)]
    # for i, chunk in enumerate(text_chunks):
    #     print(i + 1, chunk)

    return bodySents


def containsAny(line: str, AnyIncludeList: list[str]):
    if len(AnyIncludeList) == 0:
        return True
    for expr in AnyIncludeList:
        if line.find(expr) != -1:
            return True
    return False

def containsAll(line: str, MustIncludeList: list[str]):
    for expr in MustIncludeList:
        if line.find(expr) == -1:
            return False
    return True


def crawlRottenTomatoesReviews(URL: str, baseURL: str, mustIncludeAll: list[str] = [], mustIncludeAny: list[str] = [],
                               mustExcludeAll: list[str] = [], mustExcludeAny: list[str] = []):
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, features="html.parser")

    links = soup.select('a')

    outLinks = []
    #print(links)
    # Print out the result
    for link in links:
        #print(link.get_text())
        line = str(link.get('href'))
        if line != "None":
            if containsAll(line, mustIncludeAll) and containsAny(line, mustIncludeAny) \
                    and not (containsAll(line, mustExcludeAll) and containsAny(line, mustExcludeAny)):

                if 'https://' in line:
                    # print(link.get('href'))
                    outLinks.append(link.get("href"))
                else:
                    # print(baseURL + link.get('href'))
                    outLinks.append(baseURL + link.get("href"))


    print(outLinks)

    return links


def crawlRottenTomatoes(URL: str, baseURL: str, mustIncludeList: list[str]):
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, features="html.parser")

    links = soup.select('a')

    outLinks = []
    #print(links)
    # Print out the result
    for link in links:
        #print(link.get_text())
        line = str(link.get('href'))
        if line != "None":
            if containsAll(line, mustIncludeList):

                if 'https://' in line:
                    # print(link.get('href'))
                    outLinks.append(link.get("href"))
                else:
                    # print(baseURL + link.get('href'))
                    outLinks.append(baseURL + link.get("href"))
            # for expr in mustIncludeList:
            #     if line.find(expr) != -1:
            #         if 'https://' in line:
            #             # print(link.get('href'))
            #             outLinks.append(link.get("href"))
            #         else:
            #             # print(baseURL + link.get('href'))
            #             outLinks.append(baseURL + link.get("href"))

    print(outLinks)

    return links


if __name__ == '__main__':
    #test("https://gameofthrones.fandom.com/wiki/Jon_Snow")
    getBodyText("https://www.nme.com/reviews/game-thrones-season-8-episode-1-review-game-reunions-winterfell-night-king-pivots-art-installations-2476817")
    crawlRottenTomatoes("https://www.rottentomatoes.com/tv/game-of-thrones", "https://www.rottentomatoes.com", ["tv", "game-of-throne"])
    crawlRottenTomatoesReviews("https://www.rottentomatoes.com/tv/game-of-thrones/s08/reviews", "https://www.rottentomatoes.com",
                               mustExcludeAll=["rottentomatoes"])


    # Build a function to filter out links with certain keywords
    # Filter out links that contain rotten tomatoes in it at all so I can exclusively get non rotten tomatoe links





