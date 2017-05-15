#!/usr/bin/env python3

"""Validates the normalised TSV manifest files"""

import pkg_resources  # part of setuptools
version = pkg_resources.require("cgp_seq_input_val")[0].version
# python builtin
import sys
import argparse

# this project
from cgp_seq_input_val import cliutil
from cgp_seq_input_val.manifest import Manifest
from cgp_seq_input_val.manifest import ValidationError

## read variables, auto help text
parser = argparse.ArgumentParser(description='Validate a tsv import manifest file')
parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + version)
parser.add_argument('-i', '--input', dest='input', metavar='FILE',
                    help='Input manifest in tsv formats', required=True,
                    type=lambda s: cliutil.extn_check(parser, ('tsv'), s, readable=True))
parser.add_argument('-o', '--output', dest='output', metavar='DIR',
                    help='Output manifest to this area, two files (tsv, json)', required=True)
parser.add_argument('-c', '--checkfiles', dest='checkfiles', action='store_true',
                    help='When present check file exist and are non-zero size')

args = parser.parse_args()

try:
    manifest = Manifest(args.input)
    manifest.validate()
    (tsv_file, json_file) = manifest.write(args.output) # output new manifest in tsv and json.
    print("Created files:\n\t%s\n\t%s" % (tsv_file, json_file))
except ValidationError as ve:
    print("ERROR: " + str(ve), file=sys.stderr)
    exit(1)
#except (OSError, IOError) as err:
#    print("ERROR: %s - %s" % (err.strerror, err.filename), file=sys.stderr)
#    exit(err.errno)
