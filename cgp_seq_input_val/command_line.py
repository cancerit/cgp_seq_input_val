"""
Handle the command line parsing and select the correct sub process.
"""

import argparse
import sys
import pkg_resources  # part of setuptools

from cgp_seq_input_val import constants, cliutil
from cgp_seq_input_val.manifest import normalise
from cgp_seq_input_val.manifest import wrapped_validate
from cgp_seq_input_val.seq_validator import validate_seq_files
version = pkg_resources.require("cgp_seq_input_val")[0].version


def main():
    """
    Sets up the parser and handles triggereing of correct sub-command
    """
    common_parser = argparse.ArgumentParser('parent', add_help=False)
    common_parser.add_argument('-v', '--version',
                               action='version',
                               version='%(prog)s ' + version)

    parser = argparse.ArgumentParser(prog='cgpSeqInputVal', parents=[common_parser])

    subparsers = parser.add_subparsers(help='sub-command help')

    # create the parser for the "man-norm" command
    parser_a = subparsers.\
        add_parser('man-norm',
                   parents=[common_parser],
                   description='Convert manifest files to common denominator (tsv)',
                   epilog='Input can be [xls|xlsx|csv|tsv].  \
                   "tsv" is just copied to maintain tool-chain')
    parser_a.add_argument('-i', '--input',
                          dest='input',
                          metavar='FILE',
                          help='Input manifest in friendly formats',
                          required=True,
                          type=lambda s: cliutil.extn_check(parser,
                                                            constants.MANIFEST_EXTNS,
                                                            s,
                                                            readable=True))
    parser_a.add_argument('-o', '--output',
                          dest='output',
                          metavar='FILE',
                          help='Output file *.tsv [default: sub. extension]',
                          required=False,
                          type=lambda s: cliutil.extn_check(parser, ('tsv'), s))
    parser_a.set_defaults(func=normalise)

    # create the parser for the "man-valid" command
    parser_b = subparsers.add_parser('man-valid',
                                     parents=[common_parser],
                                     description='Validate a tsv import manifest file')
    parser_b.add_argument('-i', '--input',
                          dest='input',
                          metavar='FILE',
                          help='Input manifest in tsv formats',
                          required=True,
                          type=lambda s: cliutil.extn_check(parser,
                                                            ('tsv'),
                                                            s,
                                                            readable=True))
    parser_b.add_argument('-o', '--output',
                          dest='output',
                          metavar='DIR',
                          help='Output manifest to this area, two files (tsv, json)',
                          required=True)
    parser_b.add_argument('-c', '--checkfiles',
                          dest='checkfiles',
                          action='store_true',
                          help='When present check file exist and are non-zero size')
    parser_b.set_defaults(func=wrapped_validate)

    # create the parser for the "seq-valid" command
    parser_c = subparsers.add_parser('seq-valid',
                                     parents=[common_parser],
                                     description='Validates up to 2 sequencing data files.')
    parser_c.add_argument('-r', '--report',
                          dest='report',
                          type=argparse.FileType('w'),
                          default='-',
                          help='Output json report',
                          required=False)
    parser_c.add_argument('-i', '--input',
                          dest='input',
                          metavar='FILE',
                          nargs='+',
                          help='Input FASTQ (optionally gzip/bz2 compressed)',
                          required=True)
    parser_c.add_argument('-q', '--qc',
                          dest='qc',
                          type=int,
                          default=100000,
                          help='Assess phred quality scale using N pairs (0=all, slow)',
                          required=False)
    parser_c.add_argument('-o', '--output',
                          dest='output',
                          type=str,
                          help='Output as interleaved FASTQ (ignored for interleaved input)',
                          required=False)
    parser_c.set_defaults(func=validate_seq_files)

    args = parser.parse_args()
    if len(sys.argv) > 1:
        args.func(args)
    else:
        sys.exit('\nERROR Arguments required\n\tPlease run: cgpSeqInputVal --help\n')
