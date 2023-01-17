from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    user = {"name": "Clive Lucas","age" : "Non binary"}
    return  user
app.run('127.0.0.1',8080, debug=True,)
