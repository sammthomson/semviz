#!/usr/bin/env python
"""
web views for semviz

Author: Sam Thomson (sthomson@cs.cmu.edu)
"""
import os
import sys

from flask import Flask, render_template, request, jsonify
from flask.ext.wtf import Form, TextAreaField, Required

sys.path.append(os.getcwd())  # I thought this happened by default?

from semviz.services import PosTagger, SemaforClient, TurboClient


app = Flask(__name__)

SEMAFOR_CLIENT = SemaforClient.create(TurboClient(PosTagger()))


class SentenceInputForm(Form):
    sentence = TextAreaField("sentence", validators=[Required()])


@app.route("/api/v1/parse")
def parse():
    text = request.args.get('sentence', '')
    response = SEMAFOR_CLIENT.get_parses(text.split(u'\n'))
    return jsonify({"sentences": response})


@app.route("/")
def home():
    form = SentenceInputForm(csrf_enabled=False)
    return render_template('index.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
