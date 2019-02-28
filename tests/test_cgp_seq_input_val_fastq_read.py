import pytest
import os, sys, tempfile

from cgp_seq_input_val.fastq_read import FastqRead, FastqFormat, CasavaFastqRead, IlluminaFastqRead
from cgp_seq_input_val.error_classes import SeqValidationError

test_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'fastq_read')

def setup():
    pass

def teardown():
    pass


@pytest.mark.parametrize('file_name', ['bad_header_1.fq', 'bad_header_2.fq'])
def test_fastq_header_no_at(file_name):
    with pytest.raises(SeqValidationError) as e_info:
        fqi = os.path.join(test_dir, file_name)
        with open(fqi, 'r') as fp:
            fr = FastqRead(fp, 0, None)
            format = fr.get_fq_format()
    assert 'Unsupported FastQ header format' in str(e_info.value)


@pytest.mark.parametrize('file_name_format',
        zip(
            ['seq-shorter_1.fq', 'qual-shorter_1.fq', 'seq-shorter_1_casava_1_8.fq', 'qual-shorter_1_casava_1_8.fq'],
            [FastqFormat.ILLUMINA, FastqFormat.ILLUMINA, FastqFormat.CASAVA, FastqFormat.CASAVA]
        )
    )
def test_fastq_seq_shorter_than_qual(file_name_format):
    file_name, format = file_name_format

    FqClass = None
    if format == FastqFormat.ILLUMINA:
        FqClass = IlluminaFastqRead
    else:
        FqClass = CasavaFastqRead

    with pytest.raises(SeqValidationError) as e_info:
        fqi = os.path.join(test_dir, file_name)
        with open(fqi, 'r') as fp:
            fr = FqClass(fp, 0, None)
            fr.validate('x')
    assert 'appears to be corrupt' in str(e_info.value)


@pytest.mark.parametrize('file_format',
    [
        ('good_read_1.fq', FastqFormat.ILLUMINA),
        ('casava_1_8_reads.fq', FastqFormat.CASAVA)
    ])
def test_fastq_seq_determine_format(file_format):
    file_name, format = file_format
    fqi = os.path.join(test_dir, file_name)
    with open(fqi, 'r') as fp:
        fr = FastqRead(fp, 0, None)
        assert fr.get_fq_format() == format


def test_fastq_string_print():
    fqi = os.path.join(test_dir, 'good_read_1.fq')
    with open(fqi, 'r') as fp:
        fr = FastqRead(fp, 0, None)
        t = str(fr)
