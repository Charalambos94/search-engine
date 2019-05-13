from flask import Flask,render_template, request, json,redirect, url_for,session
import crawler
import file_crawler
import threading
import search_query
import search_Boolean
from werkzeug import secure_filename
import os

UPLOAD_FOLDER = str(os.getcwd()) + '/uploaded_files'
ALLOWED_EXTENSIONS = set(['txt', 'pdf'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def main():

    session['topKurl'] = {}
    return render_template('index.html')

@app.route("/search_boolean")
def search_boolean():
    return render_template('search_boolean.html')

@app.route("/search_boolean_with_arguments")
def search_boolean_with_arguments():
    return render_template('search_boolean.html', posts =  posts)


@app.route("/search_cosine")
def search_cosine():
    return render_template('index.html')

@app.route("/search_cosine_with_arguments")
def search_cosine_with_arguments():
    return render_template('index.html', posts =  posts)

@app.route("/crawl_web")
def crawl_web():
    return render_template('crawl_web.html')

@app.route("/crawl_file")
def crawl_file():
    return render_template('crawl_file.html')


@app.route("/btn_events_cos/", methods=['POST'])
def searchCosine():
    _query = request.form['cosine_query']
    _results = request.form['cosine_res']
    #session.clear()
    posts = search_query.search_v(_query,_results)
    print posts
    session['topKurl'] = posts
    print session['topKurl']
    return redirect("/search_cosine")

@app.route("/btn_events_bool/", methods=['POST'])
def searchBoolean():
    _query = request.form['boolean_query']
    _results = request.form['boolean_res']
    #session.clear()
    posts = search_Boolean.search_b(_query,_results)
    session['topBool'] = posts
    return redirect("/search_boolean")

@app.route("/btn_events_crawler/", methods=['POST'])
def crawlerEvent():
    _url = request.form['starting_url']
    urls = []
    urls.append(_url)
    t = threading.Thread(target=crawler.start_crawl,args={_url})
    t.daemon = True
    t.start()

    return redirect("/crawl_web")


@app.route("/btn_events_file_upload/", methods=['POST'])
def fileEvent():
    _file_path = request.files['file_path']
    if _file_path and allowed_file(_file_path.filename):
        filename = secure_filename(_file_path.filename)
        _file_path.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        full_path = UPLOAD_FOLDER + '/' + filename
        extension = os.path.splitext(filename)[1][1:]
        if extension == 'pdf':
            t = threading.Thread(target=file_crawler.crawl_pdf ,args=(full_path, filename))
            t.daemon = True
            t.start()
        elif extension == 'txt':
            t = threading.Thread(target=file_crawler.crawl_txt ,args=(full_path, filename))
            t.daemon = True
            t.start()

    return redirect("/crawl_file")

if __name__ == "__main__":
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(debug=False, threaded=True)
