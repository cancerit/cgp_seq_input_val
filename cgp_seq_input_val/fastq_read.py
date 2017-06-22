"""
Models a fastq read
"""

import re

from cgp_seq_input_val.error_classes import SeqValidationError

class FastqRead(object):
    """
    Models and validates a fastq read, calling print will produce a 4 line record
    regardess of original format.

    Inputs:
        fp: open file pointer to get next read from
        line_no_in: current line number
        curr_line: last line read from file
            - None = start of file
    """
    def __init__(self, fq_fh, line_no_in, curr_line):
        line_no = line_no_in
        header = None
        seq = ''
        qual = ''
        if curr_line is None:
            header = fq_fh.readline().rstrip()
            line_no_in = 1
            line_no += 1
        else:
            header = curr_line

        curr_line = fq_fh.readline().rstrip()
        line_no += 1
        while not curr_line.startswith('+'):
            seq += curr_line
            curr_line = fq_fh.readline().rstrip()
            line_no += 1

        seq_len = len(seq)
        # eat the '+' line
        curr_line = fq_fh.readline().rstrip()

        while len(qual) < seq_len:
            qual += curr_line
            curr_line = fq_fh.readline().rstrip()
            line_no += 1
            if curr_line == '':
                break
        self.header = header
        self.seq = seq
        self.qual = qual
        self.file_pos = (line_no_in, line_no)
        self.last_line = curr_line # as we need to pass this back
        self.name = None
        self.end = None

    def __str__(self):
        return "%s\n%s\n+\n%s" % (self.header, self.seq, self.qual)

    def validate(self, filename):
        """
        Checks the record read conforms to expected conventions

        Args:
            filename - filename read was read from, used in error messages

        Raises:
            SeqValidationError - Generic errror with validation
        """
        match = re.match(r'@(\S+)/([12])', self.header)
        if match is None:
            raise SeqValidationError("Sequence record header must begin with '@' \
                                     one non-whitespace character and '/[12]', line %d of %s"
                                     % (self.file_pos[0], filename))
        groups = match.groups()
        self.name = groups[0]
        self.end = groups[1]

        if len(self.qual) != len(self.seq):
            raise SeqValidationError("Fastq record at line %d of %s appears to be corrupt"
                                     % (self.file_pos[0], filename))
