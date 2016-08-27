# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from codecs import encode, decode
import urllib.request
import jieba
import jieba.posseg as pseg
import os
import sys
import nltk
from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn
import sklearn
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

'''  !!!
In python 3, bytes strings and unicode strings are now two different types. Since sockets are not aware of string encodings, they are using raw bytes strings, that have a slightly different interface from unicode strings.

So, now, whenever you have a unicode string that you need to use as a byte string, you need to encode() it. And when you have a byte string, you need to decode it to use it as a regular (python 2.x) string.

Unicode strings are quotes enclosed strings. Bytes strings are b"" enclosed strings

See What's new in python 3.0 .
'''

filteredList = ['CC', 'CD', 'DT', 'IN', 'JJ', 'JJR','JJS', 'LS', 'MD',
                'PDT', 'POS', 'PRP', 'PRP$', 'RB', 'RBR', 'RBS', 'RP', 'TO',
                'UH', 'WDT', 'WP', 'WRB']






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

        
class UrlContent:
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
        

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

class BaseURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

    def __init__(self):
        urllib.request.FancyURLopener.__init__(self)

    
    
class MyAppURLopener(BaseURLopener):
    def __init__(self):
        BaseURLopener.__init__(self)
        self._headers = {'Accept':'text/css,*/*;q=0.1',
                         'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                         'Accept-Encoding':'gzip,deflate,sdch',
                         'Accept-Language':'en-US,en;q=0.8',
                         'User-Agent':'Mozilla/5 (Solaris 10) Gecko'}

        
# Class Name: ZippedContentCrawler(AppURLopener)
class ZippedContentCrawler(MyAppURLopener):
    def __init__(self):
        super().__init__(self)
        

class IsraelNewsCrawler(MyAppURLopener):
    def __init__(self):
        MyAppURLopener.__init__(self)
        
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
        lstTarget = []
        keys = self.dictWebsites.keys()
        numEntries = len(self.dictWebsites)
        print('numEntries = ', numEntries)
        for key in keys:
            #print(self.dictWebsites[key][0])
            if dictWebsites[key] > 1:
                tup = (key, dictWebsites[key])
                if (not tup in lstTarget):
                    lstTarget.append(tup)
        for item in lstTarget:
            print(item)

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

import string
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer
from nltk.probability import FreqDist

def NLTKExTag(strWord):
    #print("NLTKExTag:strWord =" + str(strWord))
    copularVerbs = ["IS", "AM", "ARE", "WAS", "WERE", "HAS", "HAVE"]
    strUpperWord = strWord.upper()
    if strUpperWord in copularVerbs:
        print("copular: "+strWord)
        return True
    tag = nltk.pos_tag(word_tokenize(strWord))
    if tag[0][1] in filteredList:
        #print("NLTKExTag:T "+strWord)
        return True
    #print("NLTKExTag:F "+strWord)
    return False

class BINOpener(MyAppURLopener):
    def __init__(self):
        self._strURL = "http://www.breakingisraelnews.com"
        MyAppURLopener.__init__(self)
        self._lstWords = []
        self._dctWords = {}
        self._lstTarget = []
        self.strTotal = ""

    def GetResponse(self, strURL="http://www.breakingisraelnews.com"):
        response = self.open(strURL)
        self._beautifulSoup = BeautifulSoup(response.read(), "html.parser")
        self._strResult = self._beautifulSoup.prettify().encode("cp950", "ignore")

    def TrimHTMLtags(self, strSrc):
        strTarget = strSrc
        while(True):
            idxBegin = strTarget.find('<')
            if idxBegin == -1:
                break
            else:
                idxEnd   = strTarget.find('>')
                str2Remove = strTarget[idxBegin:idxEnd+1]
                strTarget = strTarget.replace(str2Remove, '')
        return strTarget

    def CalculateWF(self, paragraph):
        words = nltk.tokenize.word_tokenize(paragraph)
        self.fdist = FreqDist(words)
        print("fdist--"*8)
        keys = self.fdist.keys()
        for key in keys:
            val = self.fdist[key]
            print("[%s] = %s" % (key, val))
        self.fdist.plot(20)

    def CollectWords(self):
        self._lstAs = self._beautifulSoup.find_all('a', href=True)
        self._allLinks = self._beautifulSoup.find_all('p')

        for p in self._allLinks:
            pStr = p.decode().encode("cp950", "ignore")
            '''
            if p == None:
                print("p is None")
            if p.strip(string.whitespace) == None:
                print("p.strip is None")
            sys.stdout.flush()
            '''
            pStrDecode = pStr
            if pStrDecode != None: # and p.strip() != None:
                pStrDecode = pStrDecode.decode("utf-8", "ignore").strip(string.whitespace)

                #print("::", pStrDecode)
                pStrDecode = self.TrimHTMLtags(pStrDecode)
                #print(":::", pStrDecode)
                if (pStrDecode.find('<') == -1) and (pStrDecode.find('>') == -1):
                    self.strTotal += " "
                    self.strTotal += pStrDecode
                    print("Hello:: " + pStrDecode)
                    input("Hit enter to continue")
                    self.CollectPhrasesNsentences(pStrDecode)
            sPstr = pStr.split()    # split by WS
            
            for word in sPstr:
                if word not in self._lstWords:
                    self._lstWords.append(word)    # add new word
                    self._dctWords[word] = 1
                else:
                    self._dctWords[word] += 1            # increase count by 1
        self.CalculateWF(self.strTotal)
        # prepare target list
        keys = self._dctWords.keys()
        for key in keys:
            tup = (key, self._dctWords[key])
            strSearch = key.strip().decode("utf-8", "ignore")
            if self._dctWords[key] > 1:
                if not NLTKExTag(strSearch):
                    if not tup in self._lstTarget:
                        #print(tup)
                        self._lstTarget.append(tup)
        self._lstTarget.sort()
        print("lstTarget len:", len(self._lstTarget))
        for item in self._lstTarget:
            print(item)

    def CollectPhrasesNsentences(self, strSrc):
        self.txtTraining = state_union.raw("2005-GWBush.txt")
        self.txtSample   = state_union.raw("2006-GWBush.txt")
        self.customSentTokenizer = PunktSentenceTokenizer(self.txtTraining)
        self.lstPhsNSents = []
        self.chunkGrammar = r"""Chunk: {<RB.?>*<VB.?>*<NNP>+<NN>?}"""
        self.chunkParser = nltk.RegexpParser(self.chunkGrammar)

        tokenized = self.customSentTokenizer.tokenize(strSrc)
        try:
            for item in tokenized:
                words = nltk.word_tokenize(item)
                tagged = nltk.pos_tag(words)

                chunked = self.chunkParser.parse(tagged)
                print("---"*20)
                print(chunked)
                print("==="*20)
        except Exception as e:
            print(str(e))
        
    def CollectStatistics(self):
        self.CollectWords()
        
        
    
def testOpener():
    print(">>"*10+"iNC-breakingIsraelNews"+"<<"*10)
    url = 'http://www.breakingisraelnews.com'
    myHeaders = {'Accept':'text/css,*/*;q=0.1',
                         'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                         'Accept-Encoding':'gzip,deflate,sdch',
                         'Accept-Language':'en-US,en;q=0.8',
                         'User-Agent':'Mozilla/5 (Solaris 10) Gecko'}
    thisWork = 4
    if thisWork == 1: # WORKING
        opener = AppURLopener()
        response = opener.open(url)
        print("AFTER response")
    elif thisWork == 2: # NOT WORKING
        req = urllib.request.Request(url, headers = myHeaders)
        response = urllib.request.urlopen(req)
    elif thisWork == 3: # WORKING
        opener = BaseURLopener()
        response = opener.open(url)
        print("BaseURLopener-open(url)")
    else: #thisWork == 4:
        opener = MyAppURLopener()
        response = opener.open(url)
        print("MyAppURLopener-open(url)")
    
    
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
    lstTarget = []
    keys = dctWords.keys()
    for key in keys:
        #print("[",key ,"] = ", str(dctWords[key]))
        lnCnt += 1
        #if ((lnCnt != 0) and (lnCnt % 40 == 0)):
        #    input("Hit enter to continue")
        tup = (key, dctWords[key])
        strSearch = key.strip().decode("utf-8", "ignore")
        if (strSearch.find('<') == -1) and (strSearch.find('>') == -1):
            #print("strSearch = "+strSearch)
            if dctWords[key] > 1:
                if not NLTKExTag(strSearch):
                    if not tup in lstTarget:
                        #print(tup)
                        lstTarget.append(tup)
    lstTarget.sort()
    print("lstTarget len:", len(lstTarget))
    for item in lstTarget:
        print(item)
    print("dctLen = ", len(dctWords))
    

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
    
    #testOpener()                     working replaced with the following: BINOpener
    binOpener = BINOpener()
    binOpener.GetResponse()
    binOpener.CollectStatistics()
    
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
