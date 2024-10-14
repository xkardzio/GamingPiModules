from modules import KeyBinderService
from flask import Flask, request, jsonify
import json

BASE_URL = '/launcher-api'
kb = KeyBinderService()

app = Flask(__name__)

@app.route(f'{BASE_URL}/{kb.BASE_URL}/config', methods=['POST'])
def load_config():
    config = request.json
    kb.load_config(config)
    return jsonify({"status": "success"})

@app.route(f'{BASE_URL}/{kb.BASE_URL}/config', methods=['GET'])
def get_config():
    config = str(kb)
    return jsonify({"status" : "success", "KeyConfig" : config})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)