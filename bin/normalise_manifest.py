#!/usr/bin/env python3

# python builtin
import os, sys, argparse, stat, shutil
# this project
from cgp_seq_input_val import constants, cliutil
from cgp_seq_input_val.manifest import Manifest

## read variables, auto help text
parser = argparse.ArgumentParser(description='Convert manifest files to common denominator (tsv)',
                    epilog='Input can be [xls|xlsx|csv|tsv].  "tsv" is just copied to maintain tool-chain')
parser.add_argument('-i', '--input', dest='input', metavar='FILE',
                    help='Input manifest in friendly formats', required=True,
                    type=lambda s:cliutil.extn_check(parser, constants.MANIFEST_EXTNS, s, readable=True))
parser.add_argument('-o', '--output', dest='output', metavar='FILE',
                    help='Output file *.tsv [default: sub. extension]', required=False,
                    type=lambda s:cliutil.extn_check(parser, ('tsv'), s))
args = parser.parse_args()

# ALTERNATE SUCCESS PATHS in this block
if args.input.endswith('tsv') == True:
    if args.output is None:
        print("\nINFO: input and output will be same file, no action required\n", file=sys.stderr)
        exit(0)
    elif os.path.exists(args.output):
        # test if in/out file are the same, inode is simpler to test than stingified paths
        if_node = os.stat(args.input)[stat.ST_INO]
        of_node = os.stat(args.output)[stat.ST_INO]
        if if_node == of_node:
            print("\nINFO: input and output point to the same file, no action required\n", file=sys.stderr)
            exit(0)
        else:
            print("\nINFO: input copied to output, no format conversion required.\n", file=sys.stderr)
            shutil.copyfile(args.input, args.output, follow_symlinks=True) # will not allow dest to be a folder
            exit(0)

manifest = Manifest(args.input)
manifest.convert_by_extn(args.output)
