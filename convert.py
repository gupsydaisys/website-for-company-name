###########################################################################################
# Maps a given list of company names to their website domain names
########################################################################################### 

import urllib
import json as m_json
from urlparse import urlparse
import enchant

ENGLISH_DICT = enchant.Dict("en_US")
TRIVIAL_WORDS = ["company", "inc", "llc", "the", "of", "a", "an"]

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
    company = "".join(c for c in company if c not in ('.',','))
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

def getCompanyAcroynms(company):
    allWords = "".join([word[0] for word in company.split()]).lower()
    important = "".join([word[0] for word in company.split() if word.lower() not in TRIVIAL_WORDS]).lower()
    return [allWords] if allWords == important else [allWords, important]

# Returns the correct URL or the empty string if all provided URLS don't match
def getBestURL(company, urls):
    rankedURLSDict = {}
    for url in urls:
        simpleURL = simplifyURL(url)
        if simpleURL in rankedURLSDict:
            rankedURLSDict[simpleURL] += 1
        else:
            rankedURLSDict[simpleURL] = 1
    rankedURLSList = sorted([(k, rankedURLSDict[k]) for k in rankedURLSDict], reverse=True)
    rankedCompWordsList = arrangeWordsByImportance(company)
    companyAcroynms = getCompanyAcroynms(company)
    # print k
    # print rankedURLSList
    # print rankedCompWordsList
    # print companyAcroynms
    # print 
    for e in rankedURLSList:
        domain = e[0].split(".")[1]
        if domain in companyAcroynms:
            return e[0]
        for nonword in rankedCompWordsList[0]:
            if nonword in domain or domain in nonword:
                return e[0]
        if e[1] > 1:
            if domain in companyAcroynms:
                return e[0]
            for nonword in rankedCompWordsList[0]:
                if nonword in domain or domain in nonword:
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
                    return e[0]
            elif len(curr) <= 4:
                return e[0]

    return ""




# def matchURLToName(query2URLS):
def matchURLToName(L):
    query2URLS = {}
    for query in L:
        getURLForQuery(query, query2URLS)

    notFound = []
    out = {}
    for k in query2URLS:
        best = getBestURL(k, query2URLS[k])
        # print k
        # print query2URLS[k]
        # print best
        # print 
        if best == "":
            notFound.append(k)
        else:
            out[k] = best
    return out


######################## TESTING ##############################
# query2URLS = {}
# query2URLS["Microsoft"] = ['https://www.microsoft.com/', 'https://www.microsoft.com/en-us/download', 'https://support.microsoft.com/', 'https://en.wikipedia.org/wiki/Microsoft']
# query2URLS["National Pen Company"] = ['http://www.pens.com/national-pen-company', 'http://www.pens.com/', 'http://www.pens.com/customer-service-national-pen', 'http://www.pens.com/about-national-pen']
# query2URLS["Designzillas, LLC"] = ['http://www.designzillas.com/', 'http://www.designzillas.com/hiring', 'http://www.designzillas.com/about-us', 'http://www.designzillas.com/contact-us']
# query2URLS["California College of Arts"] = ['https://www.cca.edu/', 'https://www.cca.edu/academics', 'https://www.cca.edu/admissions', 'https://en.wikipedia.org/wiki/California_College_of_the_Arts']
# query2URLS["Flynn"] = ['http://www.flynncenter.org/', 'https://flynn.io/', 'https://en.wikipedia.org/wiki/Errol_Flynn', 'https://github.com/flynn/flynn']
d = matchURLToName(["Microsoft", "National Pen Company",
        "Designzillas, LLC", "California college of Arts", "Flynn"])
for k in d:
    print k
    print d[k]
    print 


##################### CORRECT ANSWER ##########################################
# Microsoft -> microsoft.com
# National Pen Company -> nationalpen.com
# Designzillas, LLC -> designzillas.com
# California college of Arts -> cca.edu
# Flynn -> flynn.io
