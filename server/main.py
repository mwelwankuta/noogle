from flask import Flask, request, jsonify
from database import conn
import json

app = Flask(__name__)
db = conn.cursor()


@app.route('/', methods=['POST'])
def search():
    search = request.data
    return jsonify(search)


app.run('127.0.0.1', 8080)
