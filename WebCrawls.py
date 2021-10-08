

class WebCrawls:

    def __init__(self, baseURL: str, urlList = list[str]) -> None:
        super().__init__()
        self.baseURL = baseURL
        self.urlList = urlList
        self.tfDict = dict()
        self.idfDict = dict()




