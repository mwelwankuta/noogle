from flask import Flask, request, jsonify
from database import conn
from question import question_controller
import json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def search():
    args = request.args
    return question_controller(args)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)