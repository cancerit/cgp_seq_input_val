# cgp_seq_input_val

This package is contains tools to validate manifests and validate various types
of sequence data file commonly used for NGS data.

## Design

Many components of this system are heavily driven by configuration files.  This
is to allow new validation code to be added and incorporated without modifying
the driver code.

## Tools

`cgpSeqInputVal` has multiple sub commands, listed with `cgpSeqInputVal --help`.

### cgpSeqInputVal man-norm

Takes input in multiple types and converts to tsv.  If intput is tsv just copied
the file to the output location (to simplify usage in workflows).  Valid input types
include:

* xls - Excel workbook pre-2007
* xlsx - Open Office XML workbook (Excel 2007+)
* csv - Comma separated values
* tsv - Tab sepearated values

Absolutely no validation is carried out here.

### cgpSeqInputVal man-valid

Takes the `tsv` representation of a manifest and performs validation of the structure
and data values.  The checks applied are managed by the `cgp_seq_input_val/config/*.json`
files.  Each class+version of manifest will have a config file where different requirements
and allowed values are defined.

The output is a lightly modified version of the input, adding:

* `Our Ref` - A UUID to identify this dataset

And a `json` version of the file ready for use by downstream systems.

### cgpSeqInputVal seq-valid

Takes an interleaved or a pair of paired-fastq files and produces a simple report
of:

```
{
    "interleaved": false,
    "pairs": 722079,
    "valid_q": true
}
```

Various exceptions can occur for malformed files.

The primary purpose is to confirm Sanger/Illumina 1.8+ quality scores.

#### FASTQ not BAM/CRAM

The flow of the service data will require splitting of any multi-lane BAM/CRAM files
down to the individual lanes, which we would do to interleaved fastq.  There is no
current need to parse BAM/CRAM files to check quality encoding directly as the spec
technically disallows it.  It is possible for BAM files to be incorrectly encoded
though.

## INSTALL

Installation is via `easy_install`.  Simply execute with the path to the compiled
'egg':

```bash
easy_install bundles/cgp_seq_input_val-0.1.0-py3.6.egg
```

### Package Dependancies

`easy_install` will install the relevant dependancies, listed here for convenience:

* [progressbar2](http://progressbar-2.readthedocs.io/en/latest/)
* [xlrd](https://github.com/python-excel/xlrd)

## Development environment

This project uses git pre-commit hooks.  As these will execute on your system it
is entirely up to you if you activate them.

If you want tests, coverage reports and lint-ing to automatically execute before
a commit you can activate them by running:

```
git config core.hooksPath git-hooks
```

Only a test failure will block a commit, lint-ing is not enforced (but please consider
following the guidance).

You can run the same checks manually without a commit by executing the following
in the base of the clone:

```bash
./run_tests.py
```

### Development Dependencies

#### Setup VirtualEnv

```
cd $PROJECTROOT
hash virtualenv || pip3 install virtualenv
virtualenv -p python3 env
source env/bin/activate
pip install progressbar2
pip install xlrd
python setup.py develop # so bin scripts can find module
```

For testing/coverage (`./run_tests.sh`)

```
source env/bin/activate # if not already in env
pip install pytest
pip install pytest-cov
pip install pep8
pip install radon
```

__Also see__ [Package Dependancies](#package-dependancies)

### Cutting a release

__Make sure the version is incremented__ in `./setup.py`

The release is handled by wheel:

```bash
$ source env/bin/activate # if not already
$ python setup.py bdist_wheel -d dist
# this creates an wheel archive which can be copied to a deployment location, e.g.
$ scp cgp_seq_input_val-1.1.0-py3-none-any.whl user@host:~/wheels
# on host
$ pip install --find-links=~/wheels cgp_seq_input_val
```
