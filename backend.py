from flask import Flask, request, redirect
from PIL import Image

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    """A simple index which enables people to use the api"""
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data action="/api/ephemeral">
      <input type=file name=image>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/api/ephemeral', methods=['GET', 'POST'])
def ephemeral():
    """The basic endpoint which has no persistance"""
    if request.method == 'POST':
        try:
            f = request.files['image']
            image = Image.open(f)
        except IOError:
            return "not a valid image", 400
        return get_model_output(image)
    else:
        return redirect('/')


def get_model_output(image):
    """A dummy stand-in for the model"""
    return '$2+2=4$'
