import re
import urllib
from urllib import request
import urllib.request
import nltk
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
from WebCrawls import *
from UtilityFuncts import *
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


pageNumPattern = re.compile(r"(\?page=)\d+$")


def crawlRottenTomatoesReviews(URL: str, baseURL: str, mustIncludeAll: list[str] = [], mustIncludeAny: list[str] = [],
                               mustExcludeAll: list[str] = [], mustExcludeAny: list[str] = [],
                               debug: bool = False, pageNum: int = 1, linksListLenLimit: int = 1,
                               lineLenLimit: int = 10):
    if (pageNumPattern.search(URL) != None):
        response = requests.get(URL)
    else:
        response = requests.get(URL + f"?page={pageNum}")
    soup = BeautifulSoup(response.text, features="html.parser")
    links = soup.select('a', href=True)

    outLinks = []
    for link in links:
        # print(link.get_text())
        line = str(link.get('href'))
        if line != "None" and len(line) > lineLenLimit:
            # if line.startswith("/"):
            #     line = baseURL + line
            if not line.startswith("/") and containsAll(line, mustIncludeAll) and containsAny(line, mustIncludeAny) \
                    and not (containsAll(line, mustExcludeAll) and containsAny(line, mustExcludeAny)):
                outLinks.append(line)

    if len(outLinks) < linksListLenLimit:
        return outLinks
    else:
        if debug:
            print(outLinks)
        newLinks = crawlRottenTomatoesReviews(URL, baseURL, mustIncludeAll, mustIncludeAny, mustExcludeAll,
                                              mustExcludeAny, debug, pageNum + 1, linksListLenLimit)

        outLinks.extend(newLinks)

        return outLinks


def startCrawl(urlList: list[str], baseURL: str, mustIncludeAll: list[str] = [], mustIncludeAny: list[str] = [],
               mustExcludeAll: list[str] = [], mustExcludeAny: list[str] = [],
               debug: bool = False, pageNum: int = 1, linksLenLimit: int = 1):
    crawledLinks = []
    for url in urlList:
        if debug:
            print(f"\n\nCrawls for:{url}")
        links = crawlRottenTomatoesReviews(url, baseURL, mustIncludeAll, mustIncludeAny, mustExcludeAll, mustExcludeAny,
                                           debug, pageNum, linksLenLimit)
        crawl = WebCrawls(url, links)
        crawledLinks.append(crawl)
        # if len(links) >= 0:
        #     crawledLinks.append(links)
        if debug:
            print(f"Num Crawls: {len(links)}")
    if debug:
        print(
            f"Links started with: {len(urlList)} - {urlList.__str__()}\n\n\tCrawled Links returned: {len(crawledLinks[0].urlList)}")
    return crawledLinks


directoryTokensRemovePattern = re.compile(r"[\\/:*?,`\'\"<>|&^()\{\}\(\)\[\]\%\$\#\@\!]+")
def writeOutCrawls(baseOutputDir: str, crawlsList: list[WebCrawls], replaceToken: str = "_"):
    # This function expects that whatever output directory we are at it will end in '/'
    for crawl in crawlsList:
        outDir = baseOutputDir
        folder = directoryTokensRemovePattern.sub(replaceToken, crawl.baseURL)
        outDir += folder + "/"
        for link in crawl.urlList:
            outFileName = directoryTokensRemovePattern.sub(replaceToken, link)
            with openFile(outDir + outFileName + ".txt", "w") as outFile:

                try:
                    getBodyText(link)
                except IOError:
                    print("An error occured")



if __name__ == '__main__':
    # test("https://gameofthrones.fandom.com/wiki/Jon_Snow")
    getBodyText(
        "https://www.nme.com/reviews/game-thrones-season-8-episode-1-review-game-reunions-winterfell-night-king-pivots-art-installations-2476817")

    # crawlRottenTomatoesReviews("https://www.rottentomatoes.com/tv/game-of-thrones/s08/reviews",
    #                            "https://www.rottentomatoes.com",
    #                            mustExcludeAny=["rottentomatoes", "youtube", "cookies"], pageNum=1)

    startingLinks = []
    for i in range(1, 9):
        startingLinks.append(f"https://www.rottentomatoes.com/tv/game-of-thrones/s0{i}/reviews")
    print(startingLinks)

    # startingLinks = ["https://www.rottentomatoes.com/tv/game-of-thrones/s03/reviews"]
    # crawledLinks = startCrawl(startingLinks,
    #                           "https://www.rottentomatoes.com",
    #                           mustExcludeAny=["rottentomatoes", "youtube", "cookies", "fandango"], pageNum=1,
    #                           debug=True)

    writeOutLocation = "output\\"
    cr = WebCrawls("TestBaseURL",
              ["https://www.nme.com/reviews/game-thrones-season-8-episode-1-review-game-reunions-winterfell-night-king-pivots-art-installations-2476817"])

    writeOutCrawls(writeOutLocation, [cr])
    # Build a function to filter out links with certain keywords
    # Filter out links that contain rotten tomatoes in it at all so I can exclusively get non rotten tomatoe links
