###########################################################################################
# Code from http://stackoverflow.com/questions/3898574/google-search-using-python-script #
###########################################################################################
import urllib
import json as m_json


def getURLForQuery(query):
    query = urllib.urlencode ( { 'q' : query } )
    response = urllib.urlopen ( 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query ).read()
    json = m_json.loads ( response )
    results = json [ 'responseData' ] [ 'results' ]
    # print json
    # print
    # print results
    # print
    for result in results:
        return result['url']
        title = result['title']
        url = result['url']   # was URL in the original and that threw a name error exception
        print ( title + '; ' + url )

print getURLForQuery("hello")