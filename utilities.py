import re
from nltk.stem import SnowballStemmer
from collections import Counter
# Mongo for python
import pymongo

def process_text(text):
    ps = SnowballStemmer('english')

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    # only letters allowed
    words = re.sub(r'[\W_\d+]', ' ', text).split()

    filtered_sentence = []
    for word in words:
        filtered_sentence.append(ps.stem(word))

    counted_words = Counter(filtered_sentence)

    return counted_words

def add_Inverted_Index(url, words):
    stopWords =  set(open('659-English-stopwords.txt').read().split())

    #running mongoDB locally
    client = pymongo.MongoClient('127.0.0.1', 27017)

    db = client['Inverted_Index']
    word_dict = dict(words)

    maxFreq = dict(words.most_common(1)).values()[0]

    for key, value in word_dict.items():
        tf = value/(maxFreq*1.0)
        #If word is in stopWords we punish it
        if key.lower() in stopWords:
            tf = tf * 0.05

        collection = db[key]
        # Insert new Document
        try:
             collection.insert(
                {
                    "URL": url,
                    "TFi": tf
                })
        except:
            print("Document Exists")

def update_URL_db(url ,words, title):
    client = pymongo.MongoClient('127.0.0.1', 27017)

    db = client['URLs']

    collection = db["url"]

    # insert new URL
    try:
        collection.insert_one({
            "URL": url,
            "Dist_Words": len(dict(words)),
            "Title": title,
            "Words": dict(words).keys()
        })
    except:
        print(url)
