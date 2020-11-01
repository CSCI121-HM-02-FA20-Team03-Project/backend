import base64
import json
import os

from flask import Flask, request, redirect
from PIL import Image
from psycopg2 import connect
import numpy as np
import torch

from database import encode_hex, fetch_from_database, insert_into_database
from model.infer_model import InferModel
from model.preprocess import *

app = Flask(__name__)

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    """Redirect to where they should go"""
    return redirect('/static/index.html')

@app.route('/api/ephemeral', methods=['GET', 'POST'])
def ephemeral():
    """The basic endpoint which has no persistance"""
    if request.method == 'POST':
        try:
            f = request.files['image']
            image = Image.open(f)
        except IOError:
            return "not a valid image", 400
        except KeyError:
            return "no image was provided; the files were {}.".format(str(list(request.files.keys()))), 400
        return get_model_output(image)
    else:
        return redirect('/')

@app.route('/api/upload', methods=['POST'])
def upload():
    try:
        f = request.files['image']
    except KeyError:
        return "no image was provided; the files were {}.".format(str(list(request.files.keys()))), 400
    try:
        latex = request.form['latex']
    except KeyError:
        return "no latex was provided; the form entries were {} and the files were {}.".format(str(list(request.form.keys())), str(list(request.files.keys()))), 400
    conn = connect(os.environ['DATABASE_URL'], sslmode='require')
    image = encode_hex(f)
    key = insert_into_database(conn, image, latex)
    return key

@app.route('/api/download')
def download():
    conn = connect(os.environ['DATABASE_URL'], sslmode='require')
    key = request.args.get('image')
    if key is None:
        return 'No key provided', 404
    else:
        res = fetch_from_database(conn, key)
        if res is None:
            return 'No such image', 404
        image, latex = res
        return json.dumps({ "image" : base64.b64encode(image).decode(), "latex": latex })

learned_model = InferModel()
def get_model_output(image):
    """Call the model and get the result"""
    # in_data = torch.from_numpy(np.array(image.convert("L"))).type(torch.FloatTensor)
    
    converted_image = invertImageColor(image)
    resized_image = resizeImage(converted_image)

    in_data = torch.from_numpy(np.array(resized_image)).type(torch.FloatTensor)
    prediction = learned_model.infer(in_data)
    print('Prediction: %s' % prediction)
    return prediction
