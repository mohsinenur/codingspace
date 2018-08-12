from flask import Flask, request

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def receive_message():
    if methods=='GET':
        return "Hello World!"
    else:
        return "Working Well!"


if __name__ == '__main__':
    app.run(debug=True)
