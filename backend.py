from flask import Flask, request, redirect
from PIL import Image
import numpy as np
import torch

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
