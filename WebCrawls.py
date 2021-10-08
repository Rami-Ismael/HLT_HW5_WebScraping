
from typing import List


class WebCrawls:

    def __init__(self, baseURL: str, urlList = List [ str] ) -> None:
        super().__init__()
        self.baseURL = baseURL
        self.urlList = urlList
        self.tfDict = dict()
        self.idfDict = dict()





