import sys, os, tempfile, shutil
from cgp_seq_input_val.manifest import normalise
from argparse import Namespace

data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'data')

def setup_args(indir, intype, tmpd):
    '''
    Simplifies tests by generating standardised in/out for specified filetypes
    '''
    return Namespace(input=os.path.join(indir, 'SimplifiedManifest_v1.0.%s' % (intype)),
                     output=os.path.join(tmpd, '%s_to.tsv' % (intype)) )

def setup():
    pass

def teardown():
    pass

def test_normalise_xls():
    with tempfile.TemporaryDirectory() as tmpd:
        normalise(setup_args(data_dir, 'xls', tmpd))
    pass

def test_normalise_xlsx():
    with tempfile.TemporaryDirectory() as tmpd:
        normalise(setup_args(data_dir, 'xlsx', tmpd))
    pass

def test_normalise_csv():
    with tempfile.TemporaryDirectory() as tmpd:
        normalise(setup_args(data_dir, 'csv', tmpd))
    pass

def test_normalise_tsv():
    '''
    No conversion, just copies the file
    '''
    with tempfile.TemporaryDirectory() as tmpd:
        normalise(setup_args(data_dir, 'tsv', tmpd))
    pass

def test_normalise_same_in_out_tsv():
    '''
    In and out are the same so no action taken (warning produced)
    '''
    infile = os.path.join(data_dir, 'SimplifiedManifest_v1.0.tsv')
    args = Namespace(input=infile, output=infile)
    normalise(args)
    pass

def test_normalise_no_output():
    infile = os.path.join(data_dir, 'SimplifiedManifest_v1.0.xlsx')
    with tempfile.TemporaryDirectory() as tmpd:
        shutil.copy(infile, tmpd)
        infile = os.path.join(tmpd, os.path.basename(infile))
        args = Namespace(input=infile, output=None)
        normalise(args)
    pass

def test_normalise_tsv_no_output():
    infile = os.path.join(data_dir, 'SimplifiedManifest_v1.0.tsv')
    args = Namespace(input=infile, output=None)
    normalise(args)
    pass
