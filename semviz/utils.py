"""
Author: Sam Thomson (sthomson@cs.cmu.edu)
"""
from contextlib import contextmanager
from datetime import datetime
import shutil


@contextmanager
def deleting(filename):
    """ Deletes the given file or directory at the end of the code block """
    try:
        yield filename
    finally:
        if filename:
            shutil.rmtree(filename)


def reshape(my_list, num_cols):
    """
    Reshapes a flat list into a 2d array with the given number of columns
    """
    return [my_list[i:i+num_cols] for i in range(0, len(my_list), num_cols)]



@contextmanager
def timer(clock=datetime.utcnow):
    """ Times a code block """
    start = clock()
    elapsed = {}
    try:
        yield elapsed
    finally:
        elapsed['seconds'] = (clock() - start).total_seconds()
