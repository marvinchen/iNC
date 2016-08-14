# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib.request
import jieba
import jieba.posseg as pseg
import os
import sys
import sklearn
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

def procHTTPRequest():
    urlList = [
        'http://www.breakingisraelnews.com',
        'http://www.haaretz.com',
        'http://www.jpost.com/',
        'http://www.ynetnews.com',
        'http://www.jta.org',
        'http://www.mfa.gov.il/mfa/',
        'http://www.idf.il/english/',
        'http://www.honestreporting.com',
        'http://www.globes.co.il/en/',
        'http://www.timesofisrael.com'
    ]

    url = 'http://www.emome.net/channel?chid=829&pid=1'
    request = urllib.request.Request(url)
    resp = urllib.request.urlopen(request)
    html = resp.read()
    strHTML = html.decode('cp950', 'ignore').encode('utf-8')
    print(strHTML)
    print("=="*20)
    soup = BeautifulSoup(strHTML)
    for link in soup.find_all('a'):
        print(link.get('href'))

class urlContent:
    '''
    This class resprents a scraped content via a URL. A set of urlContent objects could represent a website.
urlContent has the following functionalities:
1) Collect the URL content
2) Sorting the words of the content
3) Decide the priori of the words
4) Identify the target news via
  a) Number of the occurences
  b) Significance of the words --> ???
    '''
    def __init__(self, url):
        self.strUrl = url
        self.strUrlContent = ''
        self.dictPrioriWords = {}
        self.dictLinks = {}
        # for conversion to fileName
        self.dict2FileName = {
            ':' : 'COL',
            '/' : 'FSL',
            '\\' : 'BSL',
            '.' : 'DOT'
        }


    def url2FileName(self, url):
        '''
        : = "COL"
        / = "FSL"
        \ = "BSL"
        . = "DOT"
        '''
        # assuming url contains "http://" or "www."
        strConverted = ''
        isUrlFormat = True
        isUrlFormat = (url.find("http://") > 0) or (url.find("www.") > 0)
        if isUrlFormat:
            strConverted = url
            keys = self.dict2FileName.keys()
            for key in keys:
                strConverted = strConverted.replace(key, self.dict2FileName[key])
        return strConverted

    def lookupKey(self, val):
        keys = self.dict2FN.keys()
        for key in keys:
            if val == self.dict2FN[key]:
                return key
        return -1
        

    def getContent(self, url):
        #url = 'http://www.emome.net/channel?chid=829&pid=1'
        request = urllib.request.Request(url)
        resp = urllib.request.urlopen(request)
        html = resp.read()
        strHTML = html.decode('cp950', 'ignore').encode('utf-8')
        print(strHTML)
        # open file to save content
        
        print("=="*20)
        soup = BeautifulSoup(strHTML)
        i = 0
        for link in soup.find_all('a'):
            print(link.get('href'))
            self.dictLinks[i] = link
            i += 1
        
    def testFileName2Url(self, lstTarget):
        str2Url = lstTarget[1]
        lstKeys = list(self.dict2FileName.keys())
        lstVals = list(self.dict2FileName.values())
        indexes = range(len(lstKeys))
        for i in indexes:
            val = lstVals[i]
            key = lstKeys[i]
            str2Url = str2Url.replace(val, key)
        return str2Url

    def testUrl2FileName(self):
        keysWebsites = self.dictWebsites.keys()
        for key in keysWebsites:
            url = self.dictWebsites[key][0]
            print(key, url)
            strConverted = self.url2FileName(url)
            self.dictWebsites[key][1] = strConverted
            print('--'*15)
            print(strConverted)
            print('==>'*15)
            print(self.dictWebsites[key])
            # check for reverse function
            strFile2Url = self.testFileName2Url(self.dictWebsites[key])
            if (strFile2Url == self.dictWebsites[key][0]):
                print('[0]: '+self.dictWebsites[key][0]+' == \n')
                print('[1]: '+strFile2Url+'<==\n')
            else:
                print('[0]: '+self.dictWebsites[key][0]+' <> \n')
                print('[1]: '+strFile2Url+'<==\n')                

        #print('\n')
        #print(self.dictWebsites)
        

class IsraelNewsCrawler:
    def __init__(self):
        self.description = "This is a crawler that collects the critical current news about Israel."
        self.dictWebsites = {}
        self.numSites = len(self.dictWebsites)

        # for conversion to fileName
        self.dict2FileName = {
            ':' : 'COL',
            '/' : 'FSL',
            '\\' : 'BSL',
            '.' : 'DOT'
        }
            
        
    def addWebsite(self, url):
        values = self.dictWebsites.values()
        if (url not in values):
            key = len(self.dictWebsites)
            self.dictWebsites[key] = url


    def numSites(self):
        return self.numSites

    def describe(self, text):
        self.description = text;

    def url2FileName(self, url):
        '''
        : = "COL"
        / = "FSL"
        \ = "BSL"
        . = "DOT"
        '''
        # assuming url contains "http://" or "www."
        strConverted = ''
        isUrlFormat = True
        isUrlFormat = (url.find("http://") > 0) or (url.find("www.") > 0)
        if isUrlFormat:
            strConverted = url
            keys = self.dict2FileName.keys()
            for key in keys:
                strConverted = strConverted.replace(key, self.dict2FileName[key])
        return strConverted

    def testPrintDictWebsites(self):
        keys = self.dictWebsites.keys()
        numEntries = len(self.dictWebsites)
        print('numEntries = ', numEntries)
        for key in keys:
            print(self.dictWebsites[key][0])

    def lookupKey(self, val):
        keys = self.dict2FN.keys()
        for key in keys:
            if val == self.dict2FN[key]:
                return key
        return -1

    def testFileName2Url(self, lstTarget):
        str2Url = lstTarget[1]
        lstKeys = list(self.dict2FileName.keys())
        lstVals = list(self.dict2FileName.values())
        indexes = range(len(lstKeys))
        for i in indexes:
            val = lstVals[i]
            key = lstKeys[i]
            str2Url = str2Url.replace(val, key)
        return str2Url

    def testUrl2FileName(self):
        keysWebsites = self.dictWebsites.keys()
        for key in keysWebsites:
            url = self.dictWebsites[key][0]
            print(key, url)
            strConverted = self.url2FileName(url)
            self.dictWebsites[key].append(strConverted)
            print('--'*15)
            print(strConverted)
            print('==>'*15)
            print(self.dictWebsites[key])
            # check for reverse function
            strFile2Url = self.testFileName2Url(self.dictWebsites[key])
            if (strFile2Url == self.dictWebsites[key][0]):
                print('[0]: '+self.dictWebsites[key][0]+' == [1]: '+strFile2Url+'\n')
            else:
                print('[0]: '+self.dictWebsites[key][0]+' <> [1]: '+strFile2Url+'\n')
                
        #print('\n')
        #print(self.dictWebsites)

    def openUrlFile(self, url):
        self._request = urllib.request.urlopen(url)
        

    def getUrlContent(self, url):
        self._bs = BeautifulSoup(self._request)
        print(self._bs.prettify())

def configureCrawler(crawler):
    dictCrawler = {}
    '''dictCrawler = {
            0:['http://www.breakingisraelnews.com',''],
            1:['http://www.haaretz.com',''],
            2:['http://www.jpost.com/',''],
            3:['http://www.ynetnews.com',''],
            4:['http://www.jta.org',''],
            5:['http://www.mfa.gov.il/mfa/',''],
            6:['http://www.idf.il/english/',''],
            7:['http://www.honestreporting.com',''],
            8:['http://www.globes.co.il/en/',''],
            9:['http://www.timesofisrael.com','']
        }
    '''
    
    with open("incurls.txt") as f:
        index = 0
        for line in f:
            dictCrawler[index] = []
            dictCrawler[index].append(line.strip())
            index += 1
    keys = dictCrawler.keys()
    for key in keys:
        crawler.addWebsite(dictCrawler[key])
    
class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"
    '''
    def __init__(self):
        pass
    '''

    

def iNCMain():
    '''
    # parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.error as msg:
        print(msg)
        print("for help use --help")
        sys.exit(2)
    # process options
    for o, a in opts:
        if o in ("-h", "--help"):
            print(__doc__)
            sys.exit(0)
    # process arguments
    #for arg in args:
    #    process(arg) # process() is defined elsewhere
    '''
    ### procHTTPRequest()
    iNC = IsraelNewsCrawler()
    ''' work
    configureCrawler(iNC)
    iNC.testUrl2FileName()
    iNC.testPrintDictWebsites()
    '''
    
    print(">>"*10+"iNC-breakingIsraelNews"+"<<"*10)
    url = 'http://www.breakingisraelnews.com'
    opener = AppURLopener()
    response = opener.open(url)    #'http://httpbin.org/user-agent')
    bs = BeautifulSoup(response.read(), "html.parser")
    strRes = bs.prettify().encode("cp950", "ignore")
    lstAs = bs.find_all('a', href=True)
    # work:print(strRes)
    #for a in bs.find_all('a', href=True):
    #    print("-->URL:", a['href'])
    print("Number of entries = ", len(lstAs))

    print(">>"*10+"iNC-breakingIsraelNews"+"<<"*10)
    #allLinks = bs.select('p a[href]')
    allLinks = bs.find_all('p')
    tLen = 0
    lstWords = []
    dctWords = {}
    lnCnt = 0
    for p in allLinks:
        pStr = p.decode().encode("cp950","ignore")
        sPStr = pStr.split()
        for word in sPStr:
            if word not in lstWords:
                lstWords.append(word)
                dctWords[word] = 1
            else:
                dctWords[word] += 1
        pLen = len(pStr)
        #print("==>P:", pStr)
        tLen += pLen
    print("total len = ", tLen)
    #print(lstWords)
    keys = dctWords.keys()
    for key in keys:
        print("[",key ,"] = ", str(dctWords[key]))
        lnCnt += 1
        if ((lnCnt != 0) and (lnCnt % 40 == 0)):
            input("Hit enter to continue")
    print("dctLen = ", len(dctWords))
                         
    
    #print(bs.head.encode("cp950", "ignore"))
    #print(bs.title.encode("cp950", "ignore"))

    
    #iNC.openUrlFile(url)
    #iNC.getUrlContent(url)
    

def tfidfMain():
    with open('tf_test-Utf-8.txt', encoding="utf-8") as f:
        cor = f.readlines()
    strRes = ''
    first = True
    for c in cor:
        words = pseg.cut(c)
        for key in words:
	    #print(str(key).split('/')[0])
            if first:
                strRes = str(key).split('/')[0]
                first = False
            else:
                strRes = strRes + str(key).split('/')[0] + ' '
    corpus = strRes.strip().split('\n ')

    vectorizer=CountVectorizer()
    transformer=TfidfTransformer()
    tfidf=transformer.fit_transform(vectorizer.fit_transform(corpus))
    word=vectorizer.get_feature_names()
    weight=tfidf.toarray()  
    for i in range(len(weight)): 
        print ('Line No.', i)
        for j in range(len(word)):
            print (word[j],weight[i][j])



if __name__=='__main__':
  #tfidfMain()
  iNCMain()
