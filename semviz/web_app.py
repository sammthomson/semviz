#!/usr/bin/env python
"""
web views for semviz

Author: Sam Thomson (sthomson@cs.cmu.edu)
"""
from flask import Flask, render_template, request, jsonify
from flask.ext.wtf import Form, TextAreaField, Required

from semafor_client import SemaforClient
from malt_client import MaltClient


app = Flask(__name__)

dep_parser = MaltClient()
client = SemaforClient(dep_parser)


class SentenceInputForm(Form):
    sentence = TextAreaField("sentence", validators=[Required()])


@app.route("/api/v1/parse")
def parse():
    text = request.args.get('sentence', '')
    response = client.get_parses(text.split(u'\n'))
    return jsonify({"sentences": response})


@app.route("/")
def home():
    form = SentenceInputForm(csrf_enabled=False)
    return render_template('index.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
