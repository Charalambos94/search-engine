import urllib2
from bs4 import BeautifulSoup
import json
import requests
import re
from nltk.stem import SnowballStemmer
import utilities

# Get a List of Urls and Update the inverted Index DB and URL DB
def parse_websites(list_of_urls):
    for url in list_of_urls:
        html = urllib2.urlopen(url).read()                                     # Open website
        soup = BeautifulSoup(html,'html.parser')                               # Get html code

        for script in soup(["script", "style"]):                               # Remove all lines with sript or style tag
            script.extract()    # rip it out

        # get text
        text = soup.get_text()                                                 # Get only the text
        try:
            title = soup.title.string                                          # Get page title if exists
        except Exception as e:
            print "No title"
            title = " "                                                        # Else blank

        filtered_sentence = utilities.process_text(text)                       # Call utilities.process_text() to get filtered_sentence

        utilities.update_URL_db(url, filtered_sentence, title)                 # Call utilities.update_URL_db to update URL DB

        utilities.add_Inverted_Index(url, filtered_sentence)                   # Call utilities.add_Inverted_Index to update inverted Index

# Get starting_url and list_of_urls
# Gets all urls in starting_url and if is parseable put it in list of urls
def parseable_url(starting_url, list_of_urls):

    #[^png][^ico][^jpg][^jpeg][^pdf][^gif]
    html_page = urllib2.urlopen(starting_url)                                  # Open website
    soup = BeautifulSoup(html_page,'html.parser')                              # Get html code
    accepts = "^(http|https)://.*[^png][^ico][^jpg][^jpeg][^pdf][^gif]$"       # Not accepts pictures and pdf
    for link in soup.findAll('a', attrs={'href': re.compile(accepts)}):        # Get all links of the website
        req = urllib2.Request(link.get('href'))                                # Reguest website
        try:
            response = urllib2.urlopen(req)                                    # Check if parseable
        except urllib2.HTTPError as e:                                         # Error 'The server couldn't fulfill the request'
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
        except urllib2.URLError as e:
            print('We failed to reach a server.')                              # Error 'We failed to reach a server.'
            print('Reason: ', e.reason)
        else:
            if link.get('href') not in list_of_urls:                           # If parseable and not already in list_of_urls append
                list_of_urls.append(link.get('href'))


# Get starting_url and check if parseable
def start_crawl(starting_url):

    list_of_urls = []
    req = urllib2.Request(starting_url)                                        # Reguest website
    try:
        response = urllib2.urlopen(req)                                        # Check if parseable
    except urllib2.HTTPError as e:
        print('The server couldn\'t fulfill the request.')                     # Error 'The server couldn't fulfill the request'
        print('Error code: ', e.code)
        print "HTTPError"
        return "HTTPError"
    except urllib2.URLError as e:
        print('We failed to reach a server.')                                  # Error 'We failed to reach a server.'
        print('Reason: ', e.reason)
        print "URLError"
        return "URLError"
    else:
        list_of_urls.append(starting_url)                                      # If parseable append
        parseable_url(starting_url, list_of_urls)                              # Call parseable_url

    N = 3
    print len(list_of_urls)                                                    # For first 3 links do depth search
    if (len(list_of_urls) > N):
        for i in range(1,N):
            parseable_url(list_of_urls[i], list_of_urls)

    # print len(list_of_urls)
    #
    # print list_of_urls

    parse_websites(list_of_urls)                                               # Call parse_websites


    print("OK")
    return "OK"
