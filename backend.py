from flask import Flask, request, redirect
from PIL import Image

app = Flask(__name__)

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    """Redirect to where they should go"""
    redirect('/static/index.html')

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


def get_model_output(image):
    """A dummy stand-in for the model"""
    return '$2+2=4$'
