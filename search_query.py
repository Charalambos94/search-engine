import utilities
from collections import Counter
from collections import OrderedDict
import operator
# Mongo for python
import pymongo
import  math

# Get query and result_count and return dictionary of URL and Title
def search_v(query, result_count):
    client = pymongo.MongoClient('127.0.0.1', 27017)                           # Start mongodb locally
    invertedIndex = client['Inverted_Index']                                   # Connects with Inverted_Index DB
    urlDB = client['URLs']                                                     # Connects with URLs DB
    url_list = urlDB['url']

    if (len(result_count) == 0):                                               # If user dont give result_count initialized with 5
        result_count = 5


    url_vector = {}

    clean_query = dict(utilities.process_text(query))                          # Call utilities.process_text to get clean query

    url_weighted ={}
    N = url_list.find({}).count()*1.0                                          # Get count of all URLs we have in URLs DB
    #print ("N= ",N)

    for key,value in clean_query.items():                                      # For every distinct word of query do

        if (key in invertedIndex.collection_names()):                          # If word in Inverted_Index do
            collection = invertedIndex[key]                                    # Get query word collection in Inverted_Index
            ni = collection.find({}).count()*1.0                               # How many website includes the keyword
            key_vector = {}

            cursor = collection.find({})
            for document in cursor:
                TFi = document['TFi']*1.0                                      # Get document TFi and parse it to double
                wi = math.log10(N/ni) * TFi                                    # Calculate weight of Website

                key_vector.update({document['URL']:wi})                        # Update key_vector with URL and weight


            url_vector = Counter(url_vector) + Counter(key_vector)             # Sum weight of URL

    topURL = {}
    if (len(url_vector) != 0):
        URL_unsorted = dict(url_vector.most_common(int(result_count)))         # Get top K results and put it in a dict {URL: wi}

        URL_sorted = OrderedDict(sorted(URL_unsorted.items(), key=lambda x: x[1], reverse=True)).keys() # Sort by weight and keep URLs

        for url in URL_sorted:
            title = url_list.find_one({"URL": url})['Title']
            topURL[url_vector[url]] = url                                      # topURL {wi: URL}

        topURLsorted = OrderedDict(sorted(topURL.items(), key=lambda x: x[0], reverse=True)) # Sort by weight

        for key, value in topURLsorted.iteritems():                            # convert topURL to {wi: {page_title: URL}}
            title = url_list.find_one({"URL": value})['Title']
            topURLsorted[key] = {title: value}

    return topURLsorted
