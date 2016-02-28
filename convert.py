###########################################################################################
# Maps a given list of company names to their website domain names

# IF WGL Holdings Inc...when making acronym
#www.wglholdings.com

########################################################################################### 
import urllib
import json as m_json
from urlparse import urlparse
import enchant
import testData
import sys

URL_COUNT_WEIGHT = .25 
URL_ORDER_WEIGHT = -.25
URL_LEN_WEIGHT = -.1

ENGLISH_DICT = enchant.Dict("en_US")
TRIVIAL_WORDS = ["company", "inc", "group", "corporation", "co", "Corp", "&", "llc", "the", "of", "a", "an"]

# Code adapted from http://stackoverflow.com/questions/3898574/google-search-using-python-script #
# Assume Q is a list of unique strings
def getURLForQuery(q, query2URLS):
    query = urllib.urlencode ( { 'q' : q } )
    response = urllib.urlopen ( 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query ).read()
    json = m_json.loads ( response )
    results = json [ 'responseData' ] [ 'results' ]
    URLS = []
    for result in results:
        title = result['title']
        url = result['url']   # was URL in the original and that threw a name error exception
        URLS.append(url)
    query2URLS[q] = URLS

def simplifyURL(url):
    return urlparse(url).netloc

# Returns a list of the words in name of the company in descending order of "importance"
# Do it by length, if a word is in the dictionary, and put unimportnat words like "of" "the" "llc" at the end
def arrangeWordsByImportance(company):
    lst = sorted(company.lower().split(), key=lambda x: len(x), reverse=True)
    nonwords = []
    others = []
    for word in lst:
        # Removes trivial words
        if word in TRIVIAL_WORDS:
            continue
        # Marks words that aren't trivial and aren't in dictionary as more important
        elif not ENGLISH_DICT.check(word):
            nonwords.append(word)
        else:
            others.append(word)
    return (nonwords, others)

def getRankedURLSLst(urls):
    # store the rank of each url, rank is a linear combination of count, len of url, and order
    rankedURLSDict = {}
    min_url_rank = sys.maxint
    max_url_rank = -sys.maxint
    for i, url in enumerate(urls):
        simpleURL = simplifyURL(url)
        if simpleURL in rankedURLSDict:
            rankedURLSDict[simpleURL] = rankedURLSDict[simpleURL] + URL_COUNT_WEIGHT
        else:
            domainArr = simpleURL.split(".")
            urlSize = len(domainArr[1]) if len(domainArr) == 3 else len(domainArr[0])
            rankedURLSDict[simpleURL] = URL_COUNT_WEIGHT + URL_ORDER_WEIGHT*(i+1) + URL_LEN_WEIGHT*urlSize
        min_url_rank = min_url_rank if rankedURLSDict[simpleURL] > min_url_rank else rankedURLSDict[simpleURL]
        max_url_rank = max_url_rank if rankedURLSDict[simpleURL] < max_url_rank else rankedURLSDict[simpleURL]
    # rank by linear combination of count, len of url, and order it appears and normalize all values to be in [0, 1]
    divisor_for_url_rank = max_url_rank if max_url_rank - min_url_rank == 0 else max_url_rank - min_url_rank 
    return sorted([(k, float(rankedURLSDict[k] - min_url_rank) / divisor_for_url_rank) for k in rankedURLSDict], key=lambda x: x[1], reverse=True)

def getCompanyAcroynms(company):
    allWords = [] # acroynm comprising of the first letters of all the words
    important = [] # acroynm comprising of the first letters of all the non-trival words
    # caps = [] # acroynm comprising of any word in it's entirity and the first letter of all other words
    for word in company.split():
        allWords.append(word[0])
        # if word.isupper():
        #     caps.append(word)
        # else:
        #     caps.append(word[0])
        if word.lower() not in TRIVIAL_WORDS:
            important.append(word[0])
    return set(["".join(allWords).lower(), "".join(important).lower()]) # "".join(caps).lower()])

# Returns the correct URL or the empty string if all provided URLS don't match
def getBestURL(company, urls):
    company = "".join(c for c in company if c not in ('.',','))
    rankedURLSList = getRankedURLSLst(urls)
    for e in rankedURLSList:
        print e[0]
        print e[1]
    print
    rankedCompWordsList = arrangeWordsByImportance(company)
    companyAcroynms = getCompanyAcroynms(company)
    # print rankedURLSList
    # print rankedCompWordsList
    # print companyAcroynms
    for e in rankedURLSList:
        # normalize rank of each element
        # print e
        domainArr = e[0].split(".")
        domain = domainArr[1] if len(domainArr) == 3 else domainArr[0]
        simplifiedName = company.replace(" ", "").lower()
        if domain in simplifiedName or simplifiedName in domain:
            return (e[0], 1.0, "domain in companyName or vice versa")
        if domain in companyAcroynms:
            # print "if domain in companyAcroynms:"
            return (e[0], 1.0, "domain in comp acronyms")
        for nonword in rankedCompWordsList[0]:
            if nonword in domain or domain in nonword:
                # print "if nonword in domain or domain in nonword:"
                return e[0]
        # keep removing company words from name
        curr = domain
        for word in rankedCompWordsList[1]:
            if word in curr:
                curr = curr.replace(word, '')
        # want to be left with 3 or 4 characters 
        # but in the case of word being 4 or less characters can only be left w/ 0 or 1
        if len(domain) <= 4:
            if len(curr) <= 1:
                # print "if len(curr) <= 1:"
                return e[0]
        elif len(curr) <= 4:
            # print "elif len(curr) <= 4:"
            return e[0]

    return ""

def matchURLToName(companyNames):
    query2URLS = {}
    for query in companyNames:
        getURLForQuery(query, query2URLS)
    notFound = []
    out = {}
    for k in query2URLS:
        best = getBestURL(k, query2URLS[k])
        if best == "":
            notFound.append(k)
        else:
            out[k] = best
    return (out, notFound, query2URLS)

def getBestURLForName(query2URLS):
    notFound = []
    out = {}
    for k in query2URLS:
        best = getBestURL(k, query2URLS[k])
        if best == "":
            notFound.append(k)
        else:
            out[k] = best
    return (out, notFound)

