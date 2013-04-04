"""
Author: Sam Thomson (sthomson@cs.cmu.edu)
"""
import codecs
from contextlib import contextmanager
import os
import shutil
from tempfile import mkdtemp
from settings import SEMAFOR_HOME


@contextmanager
def deleting(filename):
    try:
        yield filename
    finally:
        if filename:
            shutil.rmtree(filename)


class MaltClient(object):
    """
    A client for retrieving dependency parses from an MaltParser executable
    """
    def get_parses(self, sentences):
        """ Gets a dependency semantic parse as conll from a sentence str. """
        with deleting(mkdtemp(suffix='XXXXXX', prefix='semafor.')) as temp_dir:
            input_filename = os.path.join(temp_dir, "sentence")
            output_filename = os.path.join(temp_dir, "conll")
            with codecs.open(input_filename, 'w', encoding="utf8") as input_file:
                input_file.write(u'\n'.join(sentences))
            os.system("cd %s && ./bin/runMalt.sh %s %s" %
                      (SEMAFOR_HOME, input_filename, temp_dir))
            with codecs.open(output_filename, encoding="utf8") as output_file:
                output = output_file.read()
            return output
