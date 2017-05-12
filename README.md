# cgp_seq_input_val

This package is contains tools to validate manifests and validate various types
of sequence data file commonly used for NGS data.

## Design

Many components of this system are heavily driven by configuration files.  This
is to allow new validation code to be added and incorporated without modifying
the driver code.

## Tools

### normalise_manifest.py

Takes input in multiple types and converts to tsv.  If intput is tsv just copied
the file to the output location (to simplify usage in workflows).  Valid input types
include:

* xls - Excel workbook pre-2007
* xlsx - Open Office XML workbook (Excel 2007+)
* csv - Comma separated values
* tsv - Tab sepearated values

Absolutely no validation is carried out here.

### validate_manifest.py

Takes the `tsv` representation of a manifest and performs validation of the structure
and data values.  The checks applied are managed by the `cgp_seq_input_val/config/*.json`
files.  Each class+version of manifest will have a config file where different requirements
and allowed values are defined.

The output is a lightly modified version of the input, adding:

* `Our Ref` - A UUID to identify this dataset

And a `json` version of the file ready for use by downstream systems.

### validate_seq_file.py

Takes an interleaved or a pair of paired-fastq files and produces a simple report of:

```
{
    "interleaved": false,
    "pairs": 722079,
    "valid_q": true
}
```

Various exceptions can occur for malformed files.

The primary purpose is to confirm Sanger/Illumina 1.8+ quality scores.

#### Why no BAM/CRAM input?

The flow of the service data will require splitting of any multi-lane BAM/CRAM files
down to the individual lanes, which we would do to interleaved fastq.  There is no
current need to parse BAM/CRAM files to check quality encoding directly as the spec
technically disallows it.  It is possible for BAM files to be incorrectly encoded though.


# INSTALL

## Dependencies

pip3 install xlrd


# Development environment

After clone cd into the project and run:

```
git config core.hooksPath git-hooks
```

## Dependencies

* python3
* nosetests-3+ (exported as `NOSETESTS3`)
* coverage
* pylint

```
pip3 install nosetests
pip3 install coverage
pip3 install pylint
```
