#!/usr/bin/env python3

"""Validates the normalised TSV manifest files"""

# python builtin
import sys
import argparse

# this project
from cgp_seq_input_val import cliutil
from cgp_seq_input_val.manifest import Manifest
from cgp_seq_input_val.manifest import ValidationError

## read variables, auto help text
parser = argparse.ArgumentParser(description='Validate a tsv import manifest file')
parser.add_argument('-i', '--input', dest='input', metavar='FILE',
                    help='Input manifest in tsv formats', required=True,
                    type=lambda s: cliutil.extn_check(parser, ('tsv'), s, readable=True))
parser.add_argument('-o', '--output', dest='output', metavar='FILE',
                    help='Output manifest augmented with UUID ref', required=True,
                    type=lambda s: cliutil.extn_check(parser, ('tsv'), s))

args = parser.parse_args()

try:
    manifest = Manifest(args.input)
    manifest.validate()
except ValidationError as ve:
    print("ERROR: " + str(ve), file=sys.stderr)
    exit(1)
