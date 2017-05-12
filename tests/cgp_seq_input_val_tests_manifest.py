from nose.tools import *
import sys, os, tempfile, shutil
from cgp_seq_input_val.manifest import Manifest, Header, ConfigError, ParsingError, ValidationError
from argparse import Namespace

data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'data')
test_data = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')
configs = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'configs')

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

### Manifest tests

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

def test_manifest_write():
    with tempfile.TemporaryDirectory() as tmpd:
        manifest = Manifest(os.path.join(test_data, 'file_set_good', 'files_good.tsv'))
        manifest.validate()
        (tsv_file, json_file) = manifest.write(tmpd) # output new manifest in tsv and json.

### Config parsing tests

@raises(ParsingError)
def test_manifest_get_config_bad_type():
     # need a good file to setup and then test get_config with a bad config file
     header = Header(os.path.join(test_data, 'good_manifest.tsv'))
     header.get_config(os.path.join(configs, 'bad_type', 'IMPORT-1.0.json'))

@raises(ParsingError)
def test_manifest_get_config_bad_version():
    # need a good file to setup and then test get_config with a bad config file
    header = Header(os.path.join(test_data, 'good_manifest.tsv'))
    header.get_config(os.path.join(configs, 'bad_version', 'IMPORT-1.0.json'))

@raises(ConfigError)
def test_manifest_json_no_body():
    # need a good file to setup and then test get_config with a bad config file
    header = Header(os.path.join(test_data, 'good_manifest.tsv'))
    header.get_config(os.path.join(configs, 'no_body', 'IMPORT-1.0.json'))

@raises(ConfigError)
def test_manifest_json_no_expected():
    # need a good file to setup and then test get_config with a bad config file
    header = Header(os.path.join(test_data, 'good_manifest.tsv'))
    header.get_config(os.path.join(configs, 'no_expected', 'IMPORT-1.0.json'))

@raises(ConfigError)
def test_manifest_json_no_header():
    # need a good file to setup and then test get_config with a bad config file
    header = Header(os.path.join(test_data, 'good_manifest.tsv'))
    header.get_config(os.path.join(configs, 'no_header', 'IMPORT-1.0.json'))

@raises(ConfigError)
def test_manifest_json_no_required():
    # need a good file to setup and then test get_config with a bad config file
    header = Header(os.path.join(test_data, 'good_manifest.tsv'))
    header.get_config(os.path.join(configs, 'no_required', 'IMPORT-1.0.json'))

@raises(ConfigError)
def test_manifest_json_no_validate():
    # need a good file to setup and then test get_config with a bad config file
    header = Header(os.path.join(test_data, 'good_manifest.tsv'))
    header.get_config(os.path.join(configs, 'no_validate', 'IMPORT-1.0.json'))

### Header tests

@raises(ValidationError)
def test_manifest_extra_header():
     # need a good file to setup and then test get_config with a bad config file
     header = Header(os.path.join(test_data, 'extraHeader.tsv'))
     config = header.get_config()
     header.validate(config['header'])

@raises(ValidationError)
def test_manifest_missing_header():
     # need a good file to setup and then test get_config with a bad config file
     header = Header(os.path.join(test_data, 'missingHeader.tsv'))
     config = header.get_config()
     header.validate(config['header'])

@raises(ValidationError)
def test_manifest_invalid_header_val():
     # need a good file to setup and then test get_config with a bad config file
     header = Header(os.path.join(test_data, 'invalidHeaderVal.tsv'))
     config = header.get_config()
     header.validate(config['header'])

### Body tests

@raises(ValidationError)
def test_manifest_invalid_body_val():
    infile = os.path.join(test_data, 'invalidBodyVal.tsv')
    manifest = Manifest(infile)
    manifest.validate()

@raises(ValidationError)
def test_manifest_absent_body_val():
    infile = os.path.join(test_data, 'absentBodyVal.tsv')
    manifest = Manifest(infile)
    manifest.validate()

@raises(ValidationError)
def test_manifest_period_body_val():
    infile = os.path.join(test_data, 'periodBodyVal.tsv')
    manifest = Manifest(infile)
    manifest.validate()

@raises(ValidationError)
def test_manifest_dup_files_same_row():
    infile = os.path.join(test_data, 'dupFilesSameRow.tsv')
    manifest = Manifest(infile)
    manifest.validate()

@raises(ValidationError)
def test_manifest_dup_files_diff_row():
    infile = os.path.join(test_data, 'dupFilesDiffRow.tsv')
    manifest = Manifest(infile)
    manifest.validate()

@raises(ValidationError)
def test_manifest_body_head_order():
    infile = os.path.join(test_data, 'bodyHeadOrder.tsv')
    manifest = Manifest(infile)
    manifest.validate()

@raises(ValidationError)
def test_manifest_extn_file1():
    infile = os.path.join(test_data, 'invalidExtnFile1.tsv')
    manifest = Manifest(infile)
    manifest.validate()

@raises(ValidationError)
def test_manifest_extn_file2():
    infile = os.path.join(test_data, 'invalidExtnFile2.tsv')
    manifest = Manifest(infile)
    manifest.validate()

@raises(ValidationError)
def test_manifest_paired_extn_mismatch():
    infile = os.path.join(test_data, 'pairedExtnMismatch.tsv')
    manifest = Manifest(infile)
    manifest.validate()

def test_manifest_file_set_good():
    infile = os.path.join(test_data, 'file_set_good',
                         'files_good.tsv')
    manifest = Manifest(infile)
    manifest.validate(True)
