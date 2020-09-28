from flask import Flask

app = Flask(__name__)

@app.route('/api/ephemeral')
def ephemeral():
    return "unimplemented"
