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

```json
{
    "interleaved": false,
    "pairs": 722079,
    "possible_encoding": [
        "Sanger",
        "Illumina 1.8"
    ],
    "quality_ascii_range": [
        37,
        67
    ],
    "valid_q": true
}
```

Optionally generates a new interleaved (gz) file when paired-fastq is the input.

Various exceptions can occur for malformed files.

The primary purpose is to confirm Sanger/Illumina 1.8+ quality scores.  Further Information
on Phred encoding can be found [here](https://en.wikipedia.org/wiki/FASTQ_format#Encoding).

#### FASTQ not BAM/CRAM

The flow of the service data will require splitting of any multi-lane BAM/CRAM files
down to the individual lanes, which we would do to interleaved fastq.  There is no
current need to parse BAM/CRAM files to check quality encoding directly as the spec
technically disallows it.  It is possible for BAM files to be incorrectly encoded
though.

## INSTALL

Installation is via `pip`.  Simply execute with the path to the packaged distribution:

```bash
pip install --find-links=~/wheels cgp_seq_input_val
# or
pip install https://github.com/cancerit/cgp_seq_input_val/archive/master.tar.gz
```

### Package Dependancies

`pip` will install the relevant dependancies, listed here for convenience:

* [progressbar2](http://progressbar-2.readthedocs.io/en/latest/)
* [xlrd](https://github.com/python-excel/xlrd)
* [xopen](https://github.com/marcelm/xopen)

## Development environment

This project uses git pre-commit hooks.  As these will execute on your system it
is entirely up to you if you activate them.

If you want tests, coverage reports and lint-ing to automatically execute before
a commit you can activate them by running:

```bash
git config core.hooksPath git-hooks
```

Only a test failure will block a commit, lint-ing is not enforced (but please consider
following the guidance).

You can run the same checks manually without a commit by executing the following
in the base of the clone:

```bash
./run_tests.sh
```

### Development Dependencies

#### Setup VirtualEnv

```bash
cd $PROJECTROOT
hash virtualenv || pip3 install virtualenv
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt
python setup.py develop # so bin scripts can find module

## If changed requirements please run:
pip freeze | grep -v `echo ${PWD##*/}` > requirements.txt
```

For testing/coverage (`./run_tests.sh`)

```bash
source env/bin/activate # if not already in env
pip install -r requirements.txt
gem install --user-install mdl
```

Test that `mdl` is available, if not add the following to your path variable:

```bash
export PATH=$HOME/.gem/ruby/X.X.X/bin:$PATH
```

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

## LICENCE

Copyright (c) 2017 Genome Research Ltd.

Author: CancerIT <cgpit@sanger.ac.uk>

This file is part of cgp_seq_input_val.

cgp_seq_input_val is free software: you can redistribute it and/or modify it under
the terms of the GNU Affero General Public License as published by the Free
Software Foundation; either version 3 of the License, or (at your option) any
later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
