#!/usr/bin/env python
"""
Author: Sam Thomson (sthomson@cs.cmu.edu)
"""
from os import system
from tempfile import mkstemp

SEMAFOR_HOME = "/Users/sam/code/semafor/semafor-semantic-parser"


def run_semafor(sentence):
    """ Run semafor on one sentence of raw text. """
    tmp_file_a = mkstemp()[1]
    tmp_file_b = mkstemp()[1]
    with open(tmp_file_a, 'w') as input_file:
        input_file.write(sentence + "\n")
    system("cd %s && ./release/fnParserDriver.sh %s %s" %
           (SEMAFOR_HOME, tmp_file_a, tmp_file_b))
    with open(tmp_file_b) as output_file:
        output_xml = output_file.read()
    system("rm %s" % tmp_file_a)
    system("rm %s" % tmp_file_b)
    return output_xml
