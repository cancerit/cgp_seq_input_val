from nose.tools import *
import sys, os, tempfile, shutil
from cgp_seq_input_val.manifest import Manifest, Header, ConfigError, ParsingError, ValidationError
from argparse import Namespace

data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'data')

def setup_args(indir, intype, tmpd):
    '''
    Simplifies tests by generating standardised in/out for specified filetypes
    '''
    return Namespace(input=os.path.join(indir, 'SimplifiedManifest_v1.0.%s' % (intype)),
                     output=os.path.join(tmpd, '%s_to.tsv' % (intype)) )

def setup():
    print("SETUP!")

def teardown():
    print("TEAR DOWN!")

@raises(ValueError)
def test_manifest_bad_filetype():
    infile = os.path.join(data_dir, 'SimplifiedManifest_v1.0.xls')
    manifest = Manifest(infile)
    manifest.validate()

@raises(ValidationError)
def test_manifest_missing_required():
     infile = os.path.join(data_dir, 'SimplifiedManifest_v1.0.tsv')
     manifest = Manifest(infile)
     manifest.validate()

@raises(ParsingError)
def test_manifest_get_config_bad_type():
     # need a good file to setup and then test get_config with a bad config file
     header = Header(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'good_manifest.tsv'))
     header.get_config(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'configs', 'bad_type', 'IMPORT-1.0.json'))

@raises(ParsingError)
def test_manifest_get_config_bad_version():
    # need a good file to setup and then test get_config with a bad config file
    header = Header(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'good_manifest.tsv'))
    header.get_config(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'configs', 'bad_version', 'IMPORT-1.0.json'))

@raises(ConfigError)
def test_manifest_json_no_body():
    # need a good file to setup and then test get_config with a bad config file
    header = Header(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'good_manifest.tsv'))
    header.get_config(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'configs', 'no_body', 'IMPORT-1.0.json'))

@raises(ConfigError)
def test_manifest_json_no_expected():
    # need a good file to setup and then test get_config with a bad config file
    header = Header(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'good_manifest.tsv'))
    header.get_config(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'configs', 'no_expected', 'IMPORT-1.0.json'))

@raises(ConfigError)
def test_manifest_json_no_header():
    # need a good file to setup and then test get_config with a bad config file
    header = Header(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'good_manifest.tsv'))
    header.get_config(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'configs', 'no_header', 'IMPORT-1.0.json'))

@raises(ConfigError)
def test_manifest_json_no_required():
    # need a good file to setup and then test get_config with a bad config file
    header = Header(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'good_manifest.tsv'))
    header.get_config(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'configs', 'no_required', 'IMPORT-1.0.json'))

@raises(ConfigError)
def test_manifest_json_no_validate():
    # need a good file to setup and then test get_config with a bad config file
    header = Header(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'good_manifest.tsv'))
    header.get_config(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'configs', 'no_validate', 'IMPORT-1.0.json'))
