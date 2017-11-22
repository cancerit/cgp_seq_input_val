import pytest
from cgp_seq_input_val.file_meta import FileValidationError, FileMeta
import os, sys, tempfile

def setup():
    pass

def teardown():
    pass

### FileMeta tests

def test_file_meta_file_absent():
    with pytest.raises(FileValidationError) as e_info:
        headers = ["Group_ID", "Sample", "Normal_Tissue", "Group_Control", "Library", "File", "File_2"]
        details = ["1", "Start", "Y", "Y", "1", "bello.bam"]
        fm = FileMeta(headers, details, '/')
        fm.test_files(1)

def test_file_meta_file_empty():
    with pytest.raises(FileValidationError) as e_info:
        headers = ["Group_ID", "Sample", "Normal_Tissue", "Group_Control", "Library", "File", "File_2"]
        details = ["1", "Start", "Y", "Y", "1", "bello.bam"]
        with tempfile.TemporaryDirectory() as tmpd:
            with open(os.path.join(tmpd, 'bello.bam'), 'w'):
                pass
            fm = FileMeta(headers, details, tmpd)
            fm.test_files(1)

def test_file_meta_get_path():
    headers = ["Group_ID", "Sample", "Normal_Tissue", "Group_Control", "Library", "File", "File_2"]
    details = ["1", "Start", "Y", "Y", "1", "bello.bam", "."]
    fm = FileMeta(headers, details, '/')
    if fm.get_path('File') == None:
        assert False
    else:
        assert True

def test_file_meta_dot_file2():
    headers = ["Group_ID", "Sample", "Normal_Tissue", "Group_Control", "Library", "File", "File_2"]
    details = ["1", "Start", "Y", "Y", "1", "bello.bam", "."]
    fm = FileMeta(headers, details, '/')
    if fm.get_path('File_2') == None:
        assert True
    else:
        assert False
