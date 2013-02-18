from flask import Flask

app = Flask(__name__)


@app.route('/upload/', methods=['POST'])
def sdist_upload():
    return 'sdist upload ok'
