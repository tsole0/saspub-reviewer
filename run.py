import os
import sys

from os.path import abspath, dirname, realpath

from src.qtgui.MainWindow.MainWindow import run_interface

def addpath(path):
    """
    Add a directory to the python path environment, and to the PYTHONPATH
    environment variable for subprocesses.
    """
    path = abspath(path)
    if 'PYTHONPATH' in os.environ:
        PYTHONPATH = path + os.pathsep + os.environ['PYTHONPATH']
    else:
        PYTHONPATH = path
    os.environ['PYTHONPATH'] = PYTHONPATH
    sys.path.insert(0, path)

def prepare():
    # Don't create *.pyc files
    sys.dont_write_bytecode = True

    # Turn numpy warnings into errors
    #import numpy; numpy.seterr(all='raise')

    # Find the directories for the source and build
    root = abspath(dirname(realpath(__file__)))

import multiprocessing
if __name__ == "__main__":
    multiprocessing.freeze_support()
    multiprocessing.set_start_method('spawn')
    prepare()

    from src.qtgui.convertUI import convert_ui
    convert_ui()

    run_interface()