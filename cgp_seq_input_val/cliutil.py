"""General command line utility functions"""
import os


def extn_check(parser, choices, fname, readable=False):
    """Checks file extensions fit expected sets

    Keyword arguments:
    readable -- When true attempt to open the file for reading
    """
    extn = os.path.splitext(fname)[1][1:]
    if readable is True:
        try:
            handle = open(fname, 'r')
            handle.close()
        except FileNotFoundError as error:
            parser.error(error)
    if extn not in choices:
        parser.error("File doesn't end with {}".format(choices))
    return fname
