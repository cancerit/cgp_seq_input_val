import pytest
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

def test_extn_check_good_extn():
    parser = argparse.ArgumentParser()
    for f in glob.glob(os.path.join(test_dir, 'good.*')):
        extn_check(parser, constants.MANIFEST_EXTNS, f, readable=True)

def test_extn_check_f_not_f():
    with pytest.raises(SystemExit) as e_info:
        parser = argparse.ArgumentParser()
        extn_check(parser, constants.MANIFEST_EXTNS, '/I_wont_exist_cgp_seq_input_val', readable=True)

def test_extn_check_bad_extn():
    with pytest.raises(SystemExit) as e_info:
        parser = argparse.ArgumentParser()
        extn_check(parser, constants.MANIFEST_EXTNS, os.path.join(test_dir, 'bad.extn'), readable=True)
