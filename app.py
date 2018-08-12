from flask import Flask, request

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])

def receive_message():
    return "Hello World!"
