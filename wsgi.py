from flask import Flask

app = Flask(__name__)

@app.route("/__ping")
def ping():
    return "PING DESDE WSGI"
