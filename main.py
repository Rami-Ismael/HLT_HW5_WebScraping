import os
import re
import socket
import urllib
from urllib import request
import urllib.request
from urllib.error import HTTPError

import nltk
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
from WebCrawls import *
from UtilityFuncts import *
import requests

from kb import KB, Profession


# import selenium
# import lxml


def pre_process(text: str):
    print(string.punctuation)

    text = text.lower()
    tokens = word_tokenize(text  )
    excludingWords = list(stopwords.words("english"))
    excludingWords.extend( list(stopwords.words("spanish")) )
    excludingWords.extend(string.punctuation)
    excludingWords.extend(string.whitespace)
    excludingWords.append("t")
    excludingWords.append("\"")
    excludingWords.append("\'")
    excludingWords.append("-")
    excludingWords.append("\'\'")
    excludingWords.append("\`")
    excludingWords.append( "n\'t")
    excludingWords.append( "\'s")
    excludingWords.append( "_")

    returnTokens = []
    for token in tokens:
        if token not in excludingWords:
            if len(token) >=3:
                returnTokens.append(token)
    return returnTokens


def frequncy(text_tokens: List[str]):
    freq_dict = dict()
    for token in text_tokens:
        if token in freq_dict.keys():
            freq_dict[token] = freq_dict[token] + 1
        else:
            freq_dict[token] = 1
    return freq_dict


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


def getBodyText(URL: str, tokensLength: int = 10, excludeAnyList: List[str] = [],DEBUG: bool = False, timeoutSeconds: int = 10):
    try:
        response = request.urlopen(URL).read().decode('utf8')
        # response = requests.get(URL, timeout=timeoutSeconds)
    except HTTPError:
        print(f"HTTP Error Exception occured when accessing {URL}... \n\tNow returning an empty List...")
        return []
    soup = BeautifulSoup(response, features="html.parser")

    # soup = BeautifulSoup(response.text, features="html.parser")
    text = soup.get_text()

    # tokens = text.splitlines()
    # newToks = [line for line in tokens if len(line.split()) > tokensLength]
    # print(newToks)
    # #print(text)

    tags = soup.body

    # bodySents = [str(line).strip() for line in soup.body.strings if len(line.strip().split()) > tokensLength
    #              and line.find("©") == -1]

    bodySents = [str(line) for line in soup.body.strings if len(line.strip().split()) > tokensLength
                 and not containsAny(line, excludeAnyList)]

    if DEBUG:
        print(bodySents)

    return bodySents


def containsAny(line: str, AnyIncludeList: List[str]):
    if len(AnyIncludeList) == 0:
        return True
    for expr in AnyIncludeList:
        if line.find(expr) != -1:
            return True
    return False


def containsAll(line: str, MustIncludeList: List[str]):
    for expr in MustIncludeList:
        if line.find(expr) == -1:
            return False
    return True


pageNumPattern = re.compile(r"(\?page=)\d+$")


def crawlRottenTomatoesReviews(URL: str, baseURL: str, mustIncludeAll: List[str] = [], mustIncludeAny: List[str] = [],
                               mustExcludeAll: List[str] = [], mustExcludeAny: List[str] = [],
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


def startCrawl(urlList: List[str], baseURL: str, mustIncludeAll: List[str] = [], mustIncludeAny: List[str] = [],
               mustExcludeAll: List[str] = [], mustExcludeAny: List[str] = [],
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


def writeOutCrawls(baseOutputDir: str, crawlsList: List[WebCrawls], excludeAnyList: List[str]= [],pickelOutputDir: str = "pickles", replaceToken: str = "_", debug: bool = False):
    # This function expects that whatever output directory we are at it will end in '/'
    webCrawlsDir = "WebCrawls"
    for crawlObj in crawlsList:
        innerFolder1 = directoryTokensRemovePattern.sub(replaceToken, crawlObj.baseURL)
        if not os.path.exists(os.path.join(os.getcwd(), pickelOutputDir, webCrawlsDir)):
            try:
                if debug:
                    print(
                        f"Path does not exist, now creating it... {os.path.join(os.getcwd(), pickelOutputDir, webCrawlsDir )}")
                os.makedirs(os.path.join(os.getcwd(), pickelOutputDir, webCrawlsDir))
            except IOError as error:
                print(error)
                continue
        writePickle(os.path.join(os.getcwd(), pickelOutputDir, webCrawlsDir, innerFolder1 + ".pickle"),
                    crawlObj, innerFolder1 + ".pickle")

        for link in crawlObj.urlList:
            outFileName = directoryTokensRemovePattern.sub(replaceToken, link) + ".txt"

            try:
                if debug:
                    print(f"Now scraping \'{link}\'")
                bodyText = getBodyText(link, excludeAnyList=excludeAnyList)
                if len(bodyText) < 1:
                    continue
            except Exception as error:
                print(error)
                continue

            if not os.path.exists(os.path.join(os.getcwd(), baseOutputDir, innerFolder1)):
                try:
                    if debug:
                        print(
                            f"Path does not exist, now creating it... {os.path.join(os.getcwd(), baseOutputDir, innerFolder1)}")
                    os.makedirs(os.path.join(os.getcwd(), baseOutputDir, innerFolder1))
                except IOError as error:
                    print(error)
                    continue

            with open(os.path.join(os.getcwd(), baseOutputDir, innerFolder1, outFileName), "w",
                      encoding="utf-8") as outFile:
                for line in bodyText:
                    outFile.write(line + "\n")


def cleanText(text: str):
    return re.sub("\s+", " ", text).strip()

def cleanTextFiles(baseDirectory: str, outputDirectory: str, debug: bool = False, processedFileModifier: str = "Proc_"):
    currentPath = os.path.join(os.getcwd(), baseDirectory)
    for filename in os.listdir(currentPath):
        innerPath = os.path.join(os.getcwd(), baseDirectory, filename)
        if os.path.isdir(innerPath):
            print(f"Now Processing / Cleaning folder {innerPath}")
            cleanTextFiles(os.path.join(baseDirectory, filename), os.path.join(outputDirectory, filename))
        elif os.path.isfile(innerPath):
            with open(innerPath, 'r', encoding="utf-8") as inFile:  # open in readonly mode
                rawText = inFile.read()
                rawText = cleanText(rawText)
                sents = nltk.sent_tokenize(rawText)

                outputPath = os.path.join(os.getcwd(), outputDirectory)
                if not os.path.exists(outputPath):
                    try:
                        if debug:
                            print(
                                f"Path does not exist, now creating it... {outputPath}")
                        os.makedirs(outputPath)
                    except IOError as error:
                        print(error)
                        continue

                with open(os.path.join(outputPath, processedFileModifier + filename), "w", encoding="utf-8") as outFile:
                    for line in sents:
                        outFile.write(line + "\n")


def create_tf_dict(text):
    tf_dict = {}
    tokens = word_tokenize(text)
    tokens = [w for w in tokens if w.isalpha() and w not in stopwords]

    # get term frequencies
    for t in tokens:
        if t in tf_dict:
            tf_dict[t] += 1
        else:
            tf_dict[t] = 1

    # get term frequencies in a more Pythonic way
    token_set = set(tokens)
    tf_dict = {t: tokens.count(t) for t in token_set}

    # normalize tf by number of tokens
    for t in tf_dict.keys():
        tf_dict[t] = tf_dict[t] / len(tokens)

    return tf_dict




if __name__ == '__main__':

    startingLinks = []
    for i in range(1, 9):
        startingLinks.append( f"https://www.rottentomatoes.com/tv/game-of-thrones/s0{i}/reviews" )
    print(f"Starting links List: \n\t{startingLinks}")
    writeOutLocation = "output"
    excludeLinksList = ["rottentomatoes", "youtube", "cookies", "fandango", "latimes", "philly.com"]
    excludeBodyLinesList = ["Company Number", "company number", "Registered Office", "registered office", "authorised and regulated", "Media Ltd", "TCA", "©"]

    needToCrawl = True
    showDebug = True
    if needToCrawl:
        crawledLinks = startCrawl(startingLinks, "https://www.rottentomatoes.com",
                                  mustExcludeAny=excludeLinksList,
                                  pageNum=1, debug=showDebug)
        writeOutCrawls(writeOutLocation, crawledLinks, excludeAnyList=excludeBodyLinesList, debug=showDebug)

    # This portion of main is meant to only be executed if there the writeOutLocation folder is present and filled with text files...

    processedWriteOutLocation = "processed_" + writeOutLocation
    cleanTextFiles(writeOutLocation, processedWriteOutLocation)


    # getBodyText("http://www.kansascity.com/entertainment/tv/article18168266.html", DEBUG=True)

    
    file_to_read = open("term_freq.pickle", "rb")


    loaded_dictionary = pickle.load(file_to_read)

    ## Choose the 10 term 
    throne = "throne"
    tyrion = "tyrion"
    stark = "stark"
    robert = "robert"
    arya = "arya"
    cersei = "cersei"
    rob  = "rob"
    emilia  = "emilia"
    melisandre = "melisandre"
    jon = "jon"
    top_term = [throne, tyrion, stark, robert , arya , cersei , rob , emilia , melisandre , jon ]

    ## add throne 
    kb = KB(Entities= dict())

    ## add throne and
    freq = loaded_dictionary["throne"]
    val = qid("throne")
    relationship = {qid("emilia"):" She wants the throne"}
    kb.add_entity( name = "throne" , freq = freq , qid = val , relationship = relationship )



    ## add tyrion
    freq = loaded_dictionary["tyrion"]
    val = qid("tyrion")
    relationship = {qid("cersia"):" younger brother of Cerseia"}
    kb.add_entity( name = "tyrion" , freq = freq , qid = val , relationship = relationship )

    ## stark
    freq = loaded_dictionary["stark"]
    val = qid("stark")
    kb.add_entity( name = "stark" , freq = freq , qid = val , relationship = None )
    kb.add_profession(val , Profession.Knight)

    ## robert
    freq = loaded_dictionary["stark"]
    val = qid("stark")
    relationship = {qid("Lord Steffon Baratheron"):" oldest son and heir of Lord Steffon Baratheon"}
    kb.add_entity( name = "stark" , freq = freq , qid = val , relationship = relationship )
    kb.add_profession(val , Profession.Lord)

    ## arya 
    freq = loaded_dictionary["arya"]
    val = qid("arya")
    kb.add_entity( name = "arya" , freq = freq , qid = val , relationship = None )

    ## cersei
    freq = loaded_dictionary["cersei"]
    val = qid("cersei")
    kb.add_entity( name = "cersei" , freq = freq , qid = val , relationship = None )

    for x in range( 5, len(top_term)):
        freq = loaded_dictionary[top_term[x]]
        val = qid(top_term[x])
        kb.add_entity( name = top_term[x] , freq = freq , qid = val , relationship = None )

    ## add rob
    kb.add_realtionship( qid("rob") , {qid("Lord Eddard Stark of Winterfell") : "The eldest sone of Eddard Stark of Winterfell"})

    ## emilia
    kb.add_realtionship(qid("emilia"), {qid("Targaryen"):"She is a Targaryen"})

    ## melisandre
    kb.add_realtionship(qid( "melisandre"), {qid("melisandre") : "She is hte Red Priestress"})
    kb.add_profession(qid("melisandre") , Profession.Priestress) 

    ## jon
    kb.add_realtionship( qid( "jon") , { qid("lyanna") : "He is the sone of Lyanna Stark " })


    kb.save_entities()
