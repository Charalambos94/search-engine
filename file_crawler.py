import re
from nltk.stem import SnowballStemmer
import utilities

from io import BytesIO
from io import StringIO

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

# Get full_path and filename of a pdf file the user want to crawl
def crawl_pdf(full_path, filename):

    rsrcmgr = PDFResourceManager()
    sio = BytesIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, sio, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    fp = open(full_path, 'rb')
    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)

    fp.close()
    text = sio.getvalue()

    filtered_sentence = utilities.process_text(text)

    full_path = "file://" + full_path

    utilities.update_URL_db(full_path, filtered_sentence, filename)

    utilities.add_Inverted_Index(full_path, filtered_sentence)

    print "OK"


# Get full_path and filename of a txt file the user want to parse
def crawl_txt(full_path, filename):
    with open(full_path) as myfile:
        data = "".join(line.rstrip() for line in myfile)                       # Read the text from text file

    filtered_sentence = utilities.process_text(data)                           # Call utilities.process_text() to clean the text file

    full_path = "file://" + full_path

    utilities.update_URL_db(full_path, filtered_sentence, filename)            # Update URL DB

    utilities.add_Inverted_Index(full_path, filtered_sentence)                 # Update Invered Index
