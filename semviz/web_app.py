#!/usr/bin/env python
"""
web views for semviz

Author: Sam Thomson (sthomson@cs.cmu.edu)
"""
from flask import Flask, render_template, flash, request, jsonify
from flask.ext.wtf import Form, TextAreaField, Required

from parse_output_xml import parse_to_dict
from run_semafor import run_semafor

app = Flask(__name__)


class SentenceInputForm(Form):
    sentence = TextAreaField("sentence", validators=[Required()])


@app.route("/api/v1/parse")
def parse():
    sentence = request.args.get('sentence', '')
    output_xml = run_semafor(sentence)
    output_dict = parse_to_dict(output_xml)
    return jsonify(output_dict)


@app.route("/")
def home():
    form = SentenceInputForm(csrf_enabled=False)
    if form.validate_on_submit():
        flash(form.sentence)
    return render_template('index.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
