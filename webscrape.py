from bs4 import BeautifulSoup
import urllib.request
import os


def testReadFile():
    fn = '/storage/sdcard0/com.hipipal.qpyplus/scripts3/GRELinks.txt'
    fd = open (fn)
    i=1
    strHeadPattern = '<a href="'
    strTailPattern = '">'
    strHFilePtn = 'page '
    strTFilePtn = '</a>'
    strFileExt = '.doc'
    for line in fd:
      #print ("\n~~~")
      #print (i, line)
      index = line.find (strHeadPattern)
      index2 = index + len (strHeadPattern)
      strHPattern = line [:index2]
      #print ("[",index,index2,"]")
      #print ("==>" + strHPattern)
      #print ("÷÷"*20)
      index3 = line.find(strTailPattern)
      strTPattern = line [index3:]
      #print ("-->" + strTPattern)
      #print ("÷÷"*20)
      strUrl = line [index2:index3]
      #print ("××>" + strUrl)
      index4 = line.find (strHFilePtn)
      index5 = line.find (strTFilePtn)
      strTargetFN = line[index4:index5]
      #strTargetFN = formatFN (strTargetFN)
      #print ("\n@@@srcFN:"+strTargetFN)
      fFN = formatFN (strTargetFN)
      print ("fFN:"+fFN)
     
      fFN = '/storage/sdcard0/com.hipipal.qpyplus/scripts3/' + strHFilePtn.rstrip () + fFN + strFileExt
      
      exTrimScrape (strUrl, fFN)
      print ('open: %s' % fFN)
      
      '''  for debugging
      i=i+1
      if (i > 5):
        break
      '''
      
      
        
def formatFN (strFN):
  ''' This converts "page 7--", "page 77", "page 477" into 
  "page007", "page077", and "page477" respectively. 
  "16--list2"
  '''
  strT = strFN
  strPtn = 'page'
  lenPtn = len (strPtn)
  lenNum = 3
  strT = strT.replace (' ', '')
  strSubT = strT [lenPtn:]
  print ('strT:'+strSubT)
  if (strSubT. isdigit ()):
    return strSubT.zfill (lenNum)
  else:
    strSubT = strSubT [0:lenPtn-1]
    print ("1else:strT:"+strSubT)
    if (strSubT. isdigit ()):
      return strSubT.zfill (lenNum)
    else:
      strSubT = strSubT [0:lenPtn-2]
      print ("2else:strT:"+strSubT)
      if (strSubT. isdigit ()):
        return strSubT.zfill (lenNum)
      else:
        return "Error"
  '''
  lenSubT = len (strSubT)
  print ("strSubT = %s len = %d" % (strSubT, lenSubT))
  srchIndx = 0
  print ("\nfortmatFN():targetStr:"+strSubT )
  # check the first non-digit
  for i in range (0, lenSubT):
    ch = strSubT [i]
    cIsdigit = ch.isdigit()
    print ("chk::", ch)
    print ("isdigit::", cIsdigit)
    if ((lenSubT == 1 and cIsdigit) or (cIsdigit == False)):
      srchIndx = i
      break
  print ("srchIndx:", srchIndx)
  strTT = strT[lenPtn:lenPtn+srchIndx+1].zfill (lenNum)
  return strPtn+strTT
  '''

def exScrape(url):
    #url = 'http://www.aflcio.org/Legislation-and-Politics/Legislative-Alerts'
    #url = 'http://www.emome.net/channel?chid=876'
    #url = 'http://xination.pixnet.net/blog/post/30855118'
    r = urllib.request.urlopen(url).read()
    rStr = r.decode()
    #print(rStr)
    return rStr
    
def exTrimScrape(url, fn):
    strPadHTMLHeader = \
    '''
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
    <html lang="zh-TW" itemscope itemtype="http://schema.org/Blog">
    <head prefix="og: http://ogp.me/ns# fb: http://ogp.me/ns/fb# article: http://ogp.me/ns/article#">
    <body>
    <div class="topbar__related-article__block topbar__related-article__block--large"
     data-articles-type="固定"
    '''
    strPadHTMLFooter = 	'''</body></html>'''

    #<div class="topbar__related-article__block topbar__related-article__block--large"
    #data-articles-type="固定"   
    #data-articles-category="進修深造"
    #data-test-variation="">
    #


    strHPtn = 'data-site-category="進修深造"'
    strTPtn = '<!-- .article-content //-->'
    rtnStr = exScrape (url)
    srchHCnt = rtnStr.count (strHPtn)
    srchTCnt = rtnStr.count (strTPtn)
    print ("cntH: ", srchHCnt)
    print ("cntT: ", srchTCnt)

    # Search for head and tail indexes to get rtnStr [indxHead:indxTail+1]
    indxHead = rtnStr.find ( strHPtn) + len ( strHPtn)
    indxTail = rtnStr.find ( strTPtn) - 1
    
    ''' for debugging
    #filename = '/storage/sdcard0/abcxyz.txt'
    target = open(fn, 'w')
    
    rStr = rtnStr [indxHead:indxTail+1]
    #Add header and footer before writing it to file
    rStr = strPadHTMLHeader + rStr + strPadHTMLFooter
    
    target.write(rStr)
    target.close()
    print ("%s created successfully." % fn)
    #print(type(soup))
    '''
    
    r = rtnStr
    soup = BeautifulSoup(r)
    #print(soup.prettify()[0:100])
    links = soup.find_all ("a")
    
    print ('numLinks found: ', len (links))
    '''
    for link in links:
        print(link.get('href'))
    '''
        


class UrlPage:
  def __init__(self, strUrl):
    self.strUrl = strUrl
    self.strPage = ''
    self.bsSoup = None
    self.strWordStats = []
    self.strLinks = []
        
  def requestUrl (self):
    resp = urllib.request.urlopen(self.strUrl).read ()
    self.strPage = resp
    strTemp = resp
    strTemp = strTemp.decode()#.decode('cp950','ignore').encode('utf-8')
    #print (strTemp)
    #print (self.strPage)
    print ("€€€"*20 )
    self.bsSoup = BeautifulSoup(self.strPage)
    self.bsSoup.prettify ()
    tLinks = self.bsSoup.find_all ('a')
    print('bs num links: ', len(tLinks))
    i=1
    for lnk in tLinks:
      self.strLinks.append(lnk.get('href'))
      print(i, lnk)
      i = i + 1

  def registerUrl(slef, url):
    self.strLinks.append(url)
        
  def analyzeStats(self):
    #print (self.strLinks [0:20])
    i = 0
    lstLen = len (self.strLinks)
    for link in self.strLinks:
      if i < lstLen:
        print (i, ' '+self.strLinks[i])
        i = i + 1
      else:
        break
        
class GREUrlPage(UrlPage):    # Level-1 url page
  def __init__(self, url):
    UrlPage.__init__(url)
    self.requestUrl(url)
    self.analyzeStats()
    self.collectTargetUrls(url)
    
  def collectTargetUrls(self, url):
    resp = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(resp)
    #print(type(soup))

    #print(soup.prettify()[0:100])
    links = soup.find_all ("a")
    
    print ('numLinks found: ', len (links))
    for link in links:
        tUrl = link.get('href')
        print('+++'+tUrl)
  
  def getLeafPageWords(url):
    print("getLeafPageWords("+url+")")
    
  def collectTargetWords(self):
    for url in self.strLinks:
      self.getLeafPageWords(url)
    
class Website:
  def __init__(self):
    self._lstUrlPages = []  # protected attribute
    self.dictWordStats = {}
    
  def registerBasePageUrl (self, urlPage):
    UrlPage(urlPage). requestUrl ()
    self._lstUrlPages.append(urlPage)
    
  def analyze (self):
    pages = self.lstUrlPages
    print(len(pages))
    for page in pages:
      print ('>>>')
      page.analyzeStats()

  def numUrls(self):
    return (len(self._lstUrlPages))
      
class GREWebsite(Website):
  def __init__(self):
    Website.__init__(self)
    self.intNumPages = 0
    self. urlPageSetBase = "http://xination.pixnet.net/blog/category/list/1330612/"
        
  def getNumPages(self):
    '''
    Specifically for "http://xination.pixnet.net/blog/category/list/1330612/"
    '''
    self.intNumPages = 10
    
    for i in range(1,11):
      url = self.urlPageSetBase + str(i)
      self.registerBasePageUrl(url)

    print('Number of urls is : ', self.numUrls())      
      
    
  def collectTargetWords(self):
    i = 1
    for item in self._lstUrlPages:
      print('###'+str(i)+item)
      i = i +1



      
def configureGRECrawler():
    '''
    <tr>
    <td class=...>...</td>
    <td calss=...>
    <td class="list-title">
    <a href="...">page 480</a>
    </td>
    <td class="...">...</td>
    <td class="...">...</td>
    </tr>
    repeat ...
    '''
    urlPageSetBase = "http://xination.pixnet.net/blog/category/list/1330612/"

def fixDoc ():
  strPadHTMLHeader = \
    '''
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
    <html lang="zh-TW" itemscope itemtype="http://schema.org/Blog">
    <head prefix="og: http://ogp.me/ns# fb: http://ogp.me/ns/fb# article: http://ogp.me/ns/article#">
    <body>'''
  folder = "/sdcard/com.hipipal.qpyplus/scripts3/"
  fn = folder + "tofixfiles.txt"
  fd = open (fn)
  strFnExt = ".doc"
  
  index = 1
  for line in fd:
    line = line.strip ()
    fn1 = folder + line + strFnExt
    print ("fn=%s" % fn1)
    fd1 = open (fn1 ).read ()
    strUqnPtn ='''<div class="article-body">'''
    
    fdFndIndex = fd1.find (strUqnPtn)
    if fdFndIndex > 0:
      strResult = strPadHTMLHeader + fd1 [ fdFndIndex :]
      #print ("fndIndex=%d, \nrStr=%s" % ( fdFndIndex , strResult ))
      fn2w = folder + line + "xx" + strFnExt
      fd2w = open (fn2w, 'w')
      print ("create: %s" % fn2w)
      fd2w.write ( strResult)
      fd2w.close ()
      
    # debugging
    #index = index + 1
    #if index > 1:
    #  break

def changeFNs ():
  folder = "/sdcard/com.hipipal.qpyplus/scripts3/"
  fn = folder + "tofixfiles.txt"
  fd = open (fn)
  strFnExt = ".doc"
  
  for line in fd:
    line = line.strip ()
    fn1 = folder + line + strFnExt
    # rename page123.doc to page123yy.doc
    # and page123xx.doc to page123.doc
    # import os
    
    fn2 = folder + line + "yy" + strFnExt
    os.rename (fn1, fn2)
    
    fn3 = folder + line + "xx" + strFnExt
    os.rename (fn3, fn1)
  
def removeYYFiles ():
  folder = "/sdcard/com.hipipal.qpyplus/scripts3/"
  fn = folder + "tofixfiles.txt"
  fd = open (fn)
  strFnExt = ".doc"
  
  for line in fd:
    line = line.strip ()
    fn1 = folder + line + strFnExt
    # remove page123yy.doc files
    # 
    
    fn2 = folder + line + "yy" + strFnExt
    print ("remove %s" % fn2)
    os.remove ( fn2)
    
class GetGREMP3:
  ''' 
  <p>
  <iframe src="https://s3.amazonaws.com/mp3_record/list38/dewplayer-playlist.swf" width="221" height="192">
  </iframe>
  </p>
  <p>
  <audio width="300" height="32" controls="controls">
    <source src="https://s3.amazonaws.com/mp3_record/list38/mp3/page+476.mp3" type="audio/mpeg" />
    Your browser does not support the
    <code>audio</code> element.
  </audio>
  </p>
  '''
    
  def __init__(self):
    '''
    51 <a href="http://xination.pixnet.net/blog/post/22187819">page 101</a>
    52 <a href="http://xination.pixnet.net/blog/post/22184792">page 100 --  哇100了</a>
    53 <a href="http://xination.pixnet.net/blog/post/22179477">page 99</a>

    become
    
    http://xination.pixnet.net/blog/post/22187819, page101.doc, page101.mp3
    http://xination.pixnet.net/blog/post/22184792, page100.doc, page100.mp3
    http://xination.pixnet.net/blog/post/22179477, page099.doc, page099.mp3
    
    '''
    self.strPathBase = "/sdcard/com.hipipal.qpyplus/scripts3/"
    self.strWebpageUrlFn = self.strPathBase + "GRELinks.txt"
    self.strResultFn = self.strPathBase + "GRERefinedLinks.txt"
    self.strMP3Fn = filename = self.strPathBase + "GREMP3Urls.txt"
    self.fdMP3 = open(self.strMP3Fn, 'w')

  def getNumFromStr (self, strAlNum):
    strT = strAlNum
    strResult = "-1"
    if strT.isdigit ():
      #print ("3:%s" % strT)
      strResult = strT
    else:
      strT = strAlNum[:-1]
      if strT.isdigit ():
        #print ("2:%s" % strT)
        strResult = strT
      else:
        strT = strAlNum[:-2]
        if strT.isdigit ():
          #print ("1:%s" % strT)
          strResult = strT
        else: # 
          strResult = "-1"
          
    strResult = strResult.zfill(3)
    return strResult
  
  
     
  def refineInputFN (self):
    str0HPtn = '53 <a href="'
    str0TPtn = '">'
    str1HPtn = 'page'
    strFnExt = '.doc'
    strMP3Ext = '.mp3'
    lenNum = 3  #for "123"
    lenPG = 4
    len0H = len ( str0HPtn)
    len0T = len ( str0TPtn)
    
    fn0 = open (self.strWebpageUrlFn )
    fn1 = open ( self.strResultFn, 'w')
    
    for line in fn0:
      aLine = line
      aLine = aLine.strip () 
      #process "page" first
      indxPage = aLine.find (str1HPtn)
      strPage = aLine [indxPage:]
      strPage = strPage.replace (' ', '')
      print ("\npageStr::%s" % strPage)
      strPnum = strPage [lenPG:(lenPG+lenNum)]
      strPnum = self.getNumFromStr( strPnum )
      print ("numStr::%s" % strPnum)
      strRfnBase = str1HPtn + strPnum 
      strFn = strRfnBase + strFnExt
      strMP3 = strRfnBase + strMP3Ext
      print ("fnStr::%s" % strFn )
      print ("mp3Str::%s" % strMP3 )
      
      #now, get the url
      str0HPtn = '53 <a href="'
      str0TPtn = '">'
      
      indxT = aLine.find ( str0TPtn)
      strUrl = aLine [len0H:indxT]
      
      aNewLine = strUrl + "," + strFn + "," + strMP3
      print ("==>::%s" % aNewLine )
      fn1.write (aNewLine+"\n")
    fn0.close ()
    fn1.close ()
  
  def getMP3url(self, strMP3url, file):
    response = urllib.request.urlopen(strMP3url)
  
    chunk16k = 16 * 1024 
    with open(file, 'wb') as f:
      while True: 
        chunk = response.read(chunk16k)
        if not chunk: 
          break 
        f.write(chunk)
    f.close()
    
  def getAmazonMP3(self, strUrl):
    strMP3UrlPtn1 = "dewplayer-playlist.swf"
    strMP3UrlPtn2 = "https://s3.amazonaws.com/mp3_record/"
    strMP3UrlPtn3 = '.mp3"'
    index1 = strUrl.find(strMP3UrlPtn1)
    strChunk1 = strUrl[index1:]
    
    index2 = strChunk1.find(strMP3UrlPtn2)
    index3 = strChunk1.find(strMP3UrlPtn3) + len(strMP3UrlPtn3)
    strChunk2 = strChunk1[index2:index3]
    #print('getAmazonMP3:>%s<' % strChunk2)
    return strChunk2

    
  def getYoutubeMP3(self, strUrl):
    #if the mp3 is not hosted in amazon, then its likely in youtube
    strMP3UrlPtnA = '<div class="article-body">'
    strMP3UrlPtnB = '<iframe src="' #https://www.youtube.com/emded/'
    strMP3UrlPtnC = '" width="'
    
    index1= strUrl.find(strMP3UrlPtnA)
    strChunk1 = strUrl[index1:]
    index2= strChunk1.find(strMP3UrlPtnB) + len(strMP3UrlPtnB)
    index3= strChunk1.find(strMP3UrlPtnC)
    strResult = strChunk1[index2:index3]
    #print('getYoutubeMP3:>%s<' % strResult)
    return strResult
    
     
  def getMP3Url (self, strWPurl):            
    strDelimiter = ","
    lstSubs = strWPurl.split(strDelimiter)
    strUrl = lstSubs[0]
    strDoc = lstSubs[1]
    strMP3 = lstSubs[2]
    #print("%s==>%s==>%s" % (strUrl,strDoc,strMP3))
    
    #get the mp3 url
    #print('urlopen>%s<' % strUrl)
    resp = urllib.request.urlopen(strUrl)
    strChunk = resp.read().decode()
    
    strUrl = ""
    strAmazonMP3Url = self.getAmazonMP3(strChunk).strip()
    strUrl = strAmazonMP3Url
    #print('strAmazonMP3Url:"%s"' % strAmazonMP3Url)
    if strUrl == "" or not strUrl:
      strYoutubeMP3Url = self.getYoutubeMP3(strChunk).strip()
      strUrl = strYoutubeMP3Url
      #print('strYoutubeMP3Url:"%s"' % strYoutubeMP3Url)

    
    print("mp3Url:>>>%s<" % strUrl)
    strUrl = strUrl + "\n"
    self.fdMP3.write(strUrl)
    #self.getMP3url(strChunk2, filename)

    
    
  def getAllMP3Urls (self):
    self.strWebpageUrlFn = "/sdcard/com.hipipal.qpyplus/scripts3/GRERefinedLinks.txt"
    ifd = open(self.strWebpageUrlFn)
    for line in ifd:
      #print('getAllMP3s>%s<' % line)
      self.getMP3Url(line)
    self.fdMP3.close()
    
  def getAllMP3(self):
    pass
    
  
    
def get1MP3 (strMP3Url):
  folder = "/sdcard/com.hipipal.qpyplus/scripts3/"
  fn = folder + "tofixfiles.txt"
  fd = open (fn)
  strFnExt = ".doc"
  
  for line in fd:
    line = line.strip ()
    fn1 = folder + line + strFnExt
    

intObjectTest = 6

def main():
  global intObjectTest
  if intObjectTest == 0:
    fixDoc ()
  elif intObjectTest == 1:
    '''
    print ("%s" % '7'.zfill(3))
    print ("%s" % '77'.zfill (3))
    '''
    testReadFile ()
  elif intObjectTest == 2:
    myWS = Website ()
    url = 'http://www.breakingisraelnews.com'
    url = 'http://xination.pixnet.net/blog/post/29164463'
    #url = 'http://www.emome.net/channel?chid=876'
    myUrlPage = UrlPage (url)
    myWS.registerUrl (myUrlPage)
    myWS.analyze ()
  elif intObjectTest == 3:
    myGREWebsite = GREWebsite()  
    myGREWebsite.getNumPages()
  elif intObjectTest == 4:
    changeFNs()
  elif intObjectTest == 5: 
    removeYYFiles()
  elif intObjectTest == 6:
    tstMP3 = GetGREMP3 ()
    #tstMP3.refineInputFN ()
    tstMP3.getAllMP3Urls()
    '''
    url = 'https://www.youtube.com/embed/DSwkD6i11c8'
    fn = "/sdcard/com.hipipal.qpyplus/scripts3/aaa.mp3"
    tstMP3.getMP3url(url, fn)
    '''
  else:
    pass
  
  
if __name__ == '__main__':
    main()