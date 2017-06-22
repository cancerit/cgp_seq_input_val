from nose.tools import *
import os, sys, tempfile

from cgp_seq_input_val.fastq_read import FastqRead
from cgp_seq_input_val.error_classes import SeqValidationError

test_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'fastq_read')

def setup():
    pass

def teardown():
    pass

@raises(SeqValidationError)
def test_fastq_header_no_at():
    fqi = os.path.join(test_dir, 'bad_header_1.fq')
    with open(fqi, 'r') as fp:
        fr = FastqRead(fp, 0, None)
        fr.validate('x')

@raises(SeqValidationError)
def test_fastq_header_at_only():
    fqi = os.path.join(test_dir, 'bad_header_2.fq')
    with open(fqi, 'r') as fp:
        fr = FastqRead(fp, 0, None)
        fr.validate('x')

@raises(SeqValidationError)
def test_fastq_seq_shorter_than_qual():
    fqi = os.path.join(test_dir, 'seq-shorter_1.fq')
    with open(fqi, 'r') as fp:
        fr = FastqRead(fp, 0, None)
        fr.validate('x')

@raises(SeqValidationError)
def test_fastq_qual_shorter_than_seq():
    fqi = os.path.join(test_dir, 'qual-shorter_1.fq')
    with open(fqi, 'r') as fp:
        fr = FastqRead(fp, 0, None)
        fr.validate('x')

def test_fastq_string_print():
    fqi = os.path.join(test_dir, 'good_read_1.fq')
    with open(fqi, 'r') as fp:
        fr = FastqRead(fp, 0, None)
        t = str(fr)
