from nose.tools import *
import os, sys, tempfile

from cgp_seq_input_val.seq_validator import SeqValidator
from cgp_seq_input_val.error_classes import SeqValidationError

test_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'fastq_read')

def setup():
    pass

def teardown():
    pass

def test_seq_val_i_read_good():
    fqi = os.path.join(test_dir, 'good_read_i.fq')
    sv = SeqValidator(fqi, None, progress_pairs=1)
    sv.validate()

def test_seq_val_p_read_good():
    fq1 = os.path.join(test_dir, 'good_read_1.fq')
    fq2 = os.path.join(test_dir, 'good_read_2.fq')
    sv = SeqValidator(fq1, fq2, progress_pairs=1)
    sv.validate()

def test_seq_val_i_gz_read_good():
    fqi = os.path.join(test_dir, 'good_read_i.fq.gz')
    sv = SeqValidator(fqi, None)
    sv.validate()
    t = str(sv)
    sv.report(sys.stdout)

def test_seq_val_p_gz_read_good():
    fq1 = os.path.join(test_dir, 'good_read_1.fq.gz')
    fq2 = os.path.join(test_dir, 'good_read_2.fq.gz')
    sv = SeqValidator(fq1, fq2)
    sv.validate()

@raises(SeqValidationError)
def test_seq_val_bad_file():
    fqi = os.path.join(test_dir, 'good_read_i.BAD')
    sv = SeqValidator(fqi, None)

@raises(SeqValidationError)
def test_seq_val_mismatch_ext():
    fq1 = os.path.join(test_dir, 'good_read_1.fq')
    fq2 = os.path.join(test_dir, 'good_read_2.fq.gz')
    sv = SeqValidator(fq1, fq2)

@raises(SeqValidationError)
def test_seq_val_more_read2():
    fq1 = os.path.join(test_dir, 'good_read_1.fq')
    fq2 = os.path.join(test_dir, '2_reads_2.fq')
    sv = SeqValidator(fq1, fq2)
    sv.validate()

@raises(SeqValidationError)
def test_seq_val_more_read1():
    fq1 = os.path.join(test_dir, '2_reads_1.fq')
    fq2 = os.path.join(test_dir, 'good_read_2.fq')
    sv = SeqValidator(fq1, fq2)
    sv.validate()

@raises(SeqValidationError)
def test_seq_val_r1_in_2():
    fq1 = os.path.join(test_dir, 'good_read_1.fq')
    fq2 = os.path.join(test_dir, 'r1_reads_in_2.fq')
    sv = SeqValidator(fq1, fq2)
    sv.validate()

@raises(SeqValidationError)
def test_seq_val_r2_in_1():
    fq1 = os.path.join(test_dir, 'good_read_2.fq')
    fq2 = os.path.join(test_dir, 'r2_reads_in_1.fq')
    sv = SeqValidator(fq1, fq2)
    sv.validate()

@raises(SeqValidationError)
def test_seq_val_fq_name():
    fq1 = os.path.join(test_dir, 'good_read_1.fq')
    fq2 = os.path.join(test_dir, 'diff_2.fq')
    sv = SeqValidator(fq1, fq2)
    sv.validate()
