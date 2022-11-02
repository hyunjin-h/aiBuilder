from flask import Flask
import dalleMega
from flask import send_file
import json
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'


@app.route('/model/<text>')
def file(text):
    res=dalleMega.dalle(text)
    return send_file(res, mimetype='image/jpeg')


app.run(host = '0.0.0.0', port=5000)