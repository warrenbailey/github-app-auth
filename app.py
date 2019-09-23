from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello from Jenkins X deploy!'


@app.route("/callback")
def callback():
    print(request)
    return "ok"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
