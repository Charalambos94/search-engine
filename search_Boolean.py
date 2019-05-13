import pymongo
import json
import ast
import pql
from collections import Counter
from itertools import islice

# Get query and result_count and return a dict with the results
def search_b(query, result_count):
    client = pymongo.MongoClient('127.0.0.1', 27017)
    invertedIndex = client['Inverted_Index']
    urlDB = client['URLs']
    url_list = urlDB['url']

    if (len(result_count) == 0):                                               # If user dont give result_count initialize with 10
        result_count = 10
    else:
        result_count = int(result_count)

    words = query.lower().split()                                              # Split query in a list

    w = []
    count = 0

    for i in words:                                                            # Find the words of the query (not the operators)
        if(i != "not" and i != "and" and i != "or"):
            i = i.replace("'","")
            w.append(i)
        elif (i == "not"):
            count += 1                                                         # Count [not] operators

    word_count = len(w)                                                        # Words count except operators
    w = dict(Counter(w)).keys()


    key_vector = []

    for key in w :                                                             # Get the URLs that consists words of the query
        if (key in invertedIndex.collection_names()):
            collection = invertedIndex[key]

            cursor = collection.find({})
            for document in cursor:

                key_vector.append(document['URL'])


    key_vector = dict(Counter(key_vector)).keys()

    for index, word in enumerate(words):
        if word == 'not':                                                      # If word after not change to ['word']
            words[index+1] = '[' + words[index+1] + ']'
        if word not in ['not', 'and', 'or']:                                   # If not boolean operator change to "Words == 'word'"
            words[index] = '(Words == ' + words[index] + ')'

    query = ' '.join(words)                                                    # Join query with space


    topURL = {}
    returnURL = {}
    if(count == word_count):                                                   # if query only consist [not] functions eg.(not 'plot' and not 'python')
        mongo_query = pql.find(query)                                          # change python boolean operation to mongodb operation
        mongo_query = json.dumps(mongo_query)                                  # convert to string
        mongo_query = mongo_query.replace("$not", "$nin")                      # when '$not' change to mongo operation '$nin' not in array
        mongo_query = ast.literal_eval(mongo_query)                            # convert to dict

        cursor = url_list.find(mongo_query)                                    # Query db with generated query

        for document in cursor:
            topURL[document['URL']] = document['Title']                        # topURL dictionary {URL, page_title}
        returnURL = {k: topURL[k] for k in topURL.keys()[:result_count]}       # return result_count URLs
    else:
        for url in key_vector:                                                 # Check only the URLs tha contain the words of the query
            exact_query = "(URL == '" + url + "') and ("+ query +")"
            mongo_query = pql.find(exact_query)                                # change python boolean operation to mongodb operation
            mongo_query = json.dumps(mongo_query)                              # convert to string
            mongo_query = mongo_query.replace("$not", "$nin")                  # when '$not' change to mongo operation '$nin' not in array
            mongo_query = ast.literal_eval(mongo_query)                        # convert to dict

            cursor = url_list.find(mongo_query)                                # Query db with generated query

            for document in cursor:
                topURL[document['URL']] = document['Title']                    # topURL dictionary {URL, page_title}

        returnURL = {k: topURL[k] for k in topURL.keys()[:result_count]}       # return result_count URLs


    return returnURL
