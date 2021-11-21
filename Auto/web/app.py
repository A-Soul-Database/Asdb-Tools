"""
Asdb Web Status
status.asdb.live
"""
from flask import Flask

app = Flask(__name__)


@app.route('/')
def Main():
    return "Hello World",200

