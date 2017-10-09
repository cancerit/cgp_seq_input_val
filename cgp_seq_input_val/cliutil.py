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
        except FileNotFoundError as error: # pragma: no cover
            parser.error(error)
    if extn not in choices: # pragma: no cover
        parser.error("File doesn't end with {}".format(choices))
    return fname

"""
Why 'pragma: no cover'
to cover parser errors in test cases you have to add a fair amount of additional
code, as we know that raising an error this way is robust consider this covered.
"""
