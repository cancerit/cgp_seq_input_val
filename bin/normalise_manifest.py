#!/usr/bin/env python3

"""Converts manifests from various types to TSV"""

import pkg_resources  # part of setuptools
version = pkg_resources.require("cgp_seq_input_val")[0].version
# python builtin
import argparse
# this project
from cgp_seq_input_val import constants, cliutil
from cgp_seq_input_val.manifest import normalise

## read variables, auto help text
parser = argparse.ArgumentParser(description='Convert manifest files to common denominator (tsv)',
                                 epilog='Input can be [xls|xlsx|csv|tsv].  "tsv" is just copied to maintain tool-chain')
parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + version)
parser.add_argument('-i', '--input', dest='input', metavar='FILE',
                    help='Input manifest in friendly formats', required=True,
                    type=lambda s: cliutil.extn_check(parser, constants.MANIFEST_EXTNS, s, readable=True))
parser.add_argument('-o', '--output', dest='output', metavar='FILE',
                    help='Output file *.tsv [default: sub. extension]', required=False,
                    type=lambda s: cliutil.extn_check(parser, ('tsv'), s))
args = parser.parse_args()

normalise(args)
