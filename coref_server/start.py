from pprint import PrettyPrinter
import json
import flask
import os
from flask import request, jsonify, render_template

app = flask.Flask(__name__)
app.config["DEBUG"] = True
pp = PrettyPrinter(indent=1)

@app.route('/analyse', methods=['GET'])
def analyse():
    result = json.loads(request.args.get("result"))
    pp.pprint(result)
    return {"text": "Hello"}


@app.route('/', methods=['GET'])
def home():
    return render_template("index.jinja")


app.run()
