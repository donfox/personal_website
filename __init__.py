from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
  return send_from_directory('static', 'index.html')

@app.route('/static/<path:path>')
def serve_static(path):
  return send_from_directory('static', path)