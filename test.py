import flask
from flask import send_file

app = flask.Flask(__name__)
app.config["DEBUG"] = True
test = "hi"
@app.route('/get_image')
def get_image():
    return send_file("img/frame.jpg", mimetype='image/jpg')
@app.route('/', methods=['GET'])
def home():
    return test
app.run(host="0.0.0.0")
