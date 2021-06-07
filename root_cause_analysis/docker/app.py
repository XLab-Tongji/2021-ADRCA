from base64 import b64encode
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import pcmci_and_walk

app = Flask(__name__)
CORS(app)


@app.route('/pcmci_and_walk', methods=['GET', 'POST'])
def pcmci_and_walk_service():
    res = request.get_json(force=True)
    res['_dataframe'] = pd.read_json(res['dataframe'])
    res.pop('dataframe')
    result = pcmci_and_walk(**res)
    return jsonify(result)


@app.route('/get_image', methods=['GET'])
def get_image():
    with open('graph.png', 'rb') as f:
        res = f.read()
    return b64encode(res)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
