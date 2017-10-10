from nose.tools import *
import os, sys, tempfile
import glob
#from argparse import Namespace

from cgp_seq_input_val.cliutil import extn_check
from cgp_seq_input_val import constants

import argparse

test_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'cliutil')

def setup():
    pass

def teardown():
    pass

def test_extn_check_good():
    parser = argparse.ArgumentParser()
    for f in glob.glob(os.path.join(test_dir, 'good.*')):
        extn_check(parser, constants.MANIFEST_EXTNS, f, readable=True)
