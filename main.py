from flask import Flask, request
from server.controller import question_controller
from crawler.crawler import *
from shared.log import logging

app = Flask(__name__)

@app.route('/api/crawler')
def crawl_for_data(ws):
    create_workers()
    crawl()

@app.route('/', methods=['GET'])
def home():
    return "Welcome to noogle search. visit /search?q=your search query to search" 

@app.route('/search', methods=['GET'])
def search():
    args = request.args
    return question_controller(args)

if __name__ == "__main__":
    app.run(debug = True)