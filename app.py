from flask import Flask, request, render_template
from server.controller import question_controller
from crawler.crawler import *

app = Flask(__name__)

@app.route('/', methods=['GET'])
def search():
    args = request.args
    query = args.get("q", None)

    if query is None:
        return render_template('search.html', search_results=[])

    search_results = question_controller(query)
    return render_template('search.html', search_results=search_results)

@app.route('/api/crawler')
def crawl_for_data(ws):
    create_workers()
    crawl()

@app.route('/api/search', methods=['GET'])
def search_endpoint():
    args = request.args
    query = args.get('q' )
    if query is None:
        return []

    return question_controller(query)

if __name__ == "__main__":
    app.run()