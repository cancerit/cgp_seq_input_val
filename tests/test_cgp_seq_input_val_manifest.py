import pytest
import sys, os, tempfile, shutil, json
from cgp_seq_input_val.manifest import Manifest, Header, Body, ConfigError, ParsingError, ValidationError
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

def test_manifest_bad_filetype():
    with pytest.raises(ValueError) as e_info:
        infile = os.path.join(data_dir, 'SimplifiedManifest_v1.0.xls')
        manifest = Manifest(infile)
        manifest.validate()

def test_manifest_missing_required():
    with pytest.raises(ValidationError) as e_info:
        infile = os.path.join(data_dir, 'SimplifiedManifest_v1.0.tsv')
        manifest = Manifest(infile)
        manifest.validate()

def test_manifest_write():
    with tempfile.TemporaryDirectory() as tmpd:
        manifest = Manifest(os.path.join(test_data, 'file_set_good', 'files_good.tsv'))
        manifest.validate()
        (tsv_file, json_file) = manifest.write(tmpd) # output new manifest in tsv and json.

def test_manifest_uuid():
    with tempfile.TemporaryDirectory() as tmpd:
        manifest = Manifest(os.path.join(test_data, 'file_set_good', 'files_good.tsv'))
        manifest.validate()
        assert manifest.get_uuid()

def test_manifest_existing_uuid():
    with tempfile.TemporaryDirectory() as tmpd:
        manifest = Manifest(os.path.join(test_data, 'with_uuid.tsv'))
        manifest.validate()
        assert manifest.get_uuid() == '05218fd0-79e5-4214-92d5-e133cd16a798'

def test_manifest_existing_bad_uuid():
    with pytest.raises(ValidationError) as e_info:
        with tempfile.TemporaryDirectory() as tmpd:
            manifest = Manifest(os.path.join(test_data, 'with_bad_uuid.tsv'))
            manifest.validate()

def test_manifest_uuid_novalidate():
    with pytest.raises(ValidationError) as e_info:
        with tempfile.TemporaryDirectory() as tmpd:
            manifest = Manifest(os.path.join(test_data, 'file_set_good', 'files_good.tsv'))
            assert manifest.get_uuid()

### Config parsing tests

def test_manifest_get_config_bad_type():
    with pytest.raises(ParsingError) as e_info:
        # need a good file to setup and then test get_config with a bad config file
        header = Header(os.path.join(test_data, 'good_manifest.tsv'))
        header.get_config(os.path.join(configs, 'bad_type', 'IMPORT-1.0.json'))

def test_manifest_get_config_bad_version():
    with pytest.raises(ParsingError) as e_info:
        # need a good file to setup and then test get_config with a bad config file
        header = Header(os.path.join(test_data, 'good_manifest.tsv'))
        header.get_config(os.path.join(configs, 'bad_version', 'IMPORT-1.0.json'))

def test_manifest_json_no_body():
    with pytest.raises(ConfigError) as e_info:
        # need a good file to setup and then test get_config with a bad config file
        header = Header(os.path.join(test_data, 'good_manifest.tsv'))
        header.get_config(os.path.join(configs, 'no_body', 'IMPORT-1.0.json'))

def test_manifest_json_no_expected():
    with pytest.raises(ConfigError) as e_info:
        # need a good file to setup and then test get_config with a bad config file
        header = Header(os.path.join(test_data, 'good_manifest.tsv'))
        header.get_config(os.path.join(configs, 'no_expected', 'IMPORT-1.0.json'))

def test_manifest_json_no_header():
    with pytest.raises(ConfigError) as e_info:
        # need a good file to setup and then test get_config with a bad config file
        header = Header(os.path.join(test_data, 'good_manifest.tsv'))
        header.get_config(os.path.join(configs, 'no_header', 'IMPORT-1.0.json'))

def test_manifest_json_no_required():
    with pytest.raises(ConfigError) as e_info:
        # need a good file to setup and then test get_config with a bad config file
        header = Header(os.path.join(test_data, 'good_manifest.tsv'))
        header.get_config(os.path.join(configs, 'no_required', 'IMPORT-1.0.json'))

def test_manifest_json_no_validate():
    with pytest.raises(ConfigError) as e_info:
        # need a good file to setup and then test get_config with a bad config file
        header = Header(os.path.join(test_data, 'good_manifest.tsv'))
        header.get_config(os.path.join(configs, 'no_validate', 'IMPORT-1.0.json'))

def test_manifest_json_limit_no_limit_by():
    with pytest.raises(ConfigError) as e_info:
        # need a good file to setup and then test get_config with a bad config file
        infile = os.path.join(test_data,
                             'file_set_good',
                             'files_good.tsv')
        header = Header(infile)
        cfg = header.get_config(os.path.join(configs, 'limit_no_limit_by', 'IMPORT-1.0.json'))
        body = Body(infile, cfg['body'])
        body.validate(cfg['body'])

def test_manifest_json_limit_by_no_limit():
    with pytest.raises(ConfigError) as e_info:
        # need a good file to setup and then test get_config with a bad config file
        infile = os.path.join(test_data,
                             'file_set_good',
                             'files_good.tsv')
        header = Header(infile)
        cfg = header.get_config(os.path.join(configs, 'limit_by_no_limit', 'IMPORT-1.0.json'))
        body = Body(infile, cfg['body'])
        body.validate(cfg['body'])

### Header tests

def test_manifest_extra_header():
    with pytest.raises(ValidationError) as e_info:
        # need a good file to setup and then test get_config with a bad config file
        header = Header(os.path.join(test_data, 'extraHeader.tsv'))
        config = header.get_config()
        header.validate(config['header'])

def test_manifest_missing_header():
    with pytest.raises(ValidationError) as e_info:
        # need a good file to setup and then test get_config with a bad config file
        header = Header(os.path.join(test_data, 'missingHeader.tsv'))
        config = header.get_config()
        header.validate(config['header'])

def test_manifest_invalid_header_val():
    with pytest.raises(ValidationError) as e_info:
        # need a good file to setup and then test get_config with a bad config file
        header = Header(os.path.join(test_data, 'invalidHeaderVal.tsv'))
        config = header.get_config()
        header.validate(config['header'])

### Body tests

def test_manifest_invalid_body_val():
    with pytest.raises(ValidationError) as e_info:
        infile = os.path.join(test_data, 'invalidBodyVal.tsv')
        manifest = Manifest(infile)
        manifest.validate()

def test_manifest_absent_body_val():
    with pytest.raises(ValidationError) as e_info:
        infile = os.path.join(test_data, 'absentBodyVal.tsv')
        manifest = Manifest(infile)
        manifest.validate()

def test_manifest_period_body_val():
    with pytest.raises(ValidationError) as e_info:
        infile = os.path.join(test_data, 'periodBodyVal.tsv')
        manifest = Manifest(infile)
        manifest.validate()

def test_manifest_dup_files_same_row():
    with pytest.raises(ValidationError) as e_info:
        infile = os.path.join(test_data, 'dupFilesSameRow.tsv')
        manifest = Manifest(infile)
        manifest.validate()

def test_manifest_dup_files_diff_row():
    with pytest.raises(ValidationError) as e_info:
        infile = os.path.join(test_data, 'dupFilesDiffRow.tsv')
        manifest = Manifest(infile)
        manifest.validate()

def test_manifest_body_head_order():
    with pytest.raises(ValidationError) as e_info:
        infile = os.path.join(test_data, 'bodyHeadOrder.tsv')
        manifest = Manifest(infile)
        manifest.validate()

def test_manifest_extn_file1():
    with pytest.raises(ValidationError) as e_info:
        infile = os.path.join(test_data, 'invalidExtnFile1.tsv')
        manifest = Manifest(infile)
        manifest.validate()

def test_manifest_extn_file2():
    with pytest.raises(ValidationError) as e_info:
        infile = os.path.join(test_data, 'invalidExtnFile2.tsv')
        manifest = Manifest(infile)
        manifest.validate()

def test_manifest_paired_extn_mismatch():
    with pytest.raises(ValidationError) as e_info:
        infile = os.path.join(test_data, 'pairedExtnMismatch.tsv')
        manifest = Manifest(infile)
        manifest.validate()

def test_manifest_limit_exceeded():
    with pytest.raises(ValidationError) as e_info:
        # need a good file to setup and then test get_config with a bad config file
        infile = os.path.join(test_data,
                             'file_set_good',
                             'files_good.tsv')
        header = Header(infile)
        cfg = header.get_config(os.path.join(configs, 'limit_to_exceed', 'IMPORT-1.0.json'))
        body = Body(infile, cfg['body'])
        body.validate(cfg['body'])

def test_manifest_file_set_good():
    infile = os.path.join(test_data, 'file_set_good',
                         'files_good.tsv')
    manifest = Manifest(infile)
    manifest.validate(True)
    as_json = json.dumps(manifest.for_json())
