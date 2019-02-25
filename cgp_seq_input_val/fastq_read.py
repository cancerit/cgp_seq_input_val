"""
Models a fastq read
"""

import re
from enum import Enum
from cgp_seq_input_val.error_classes import SeqValidationError

ILLUMINA_FASTQ_HEADER_PATTERN = r'^@(\S+)/([12])$'
CASAVA_FASTQ_HEADER_PATTERN = r'^@(\S+)\s([12])(:\w+:\w+:\w+)$'


class FastqFormat(Enum):
    ILLUMINA = 'Illumina'
    CASAVA = 'Casava_1.8'


class FastqRead(object):
    """
    Models and validates a fastq read, calling print will produce a 4 line
    record regardess of original format.

    Inputs:
        fp: open file pointer to get next read from
        line_no_in: current line number
        curr_line: last line read from file
            - None = start of file
    """
    def __init__(self, fq_fh, line_no_in, curr_line, format):
        line_no = line_no_in
        seq_header = None
        seq = ''
        qual = ''
        if curr_line is None:
            seq_header = fq_fh.readline().rstrip()
            line_no_in = 1
            line_no += 1
        else:
            seq_header = curr_line

        if format is None:
            if re.match(ILLUMINA_FASTQ_HEADER_PATTERN, seq_header) is not None:
                format = FastqFormat.ILLUMINA
            elif re.match(CASAVA_FASTQ_HEADER_PATTERN, seq_header) is not None:
                format = FastqFormat.CASAVA
            else:
                raise SeqValidationError("Unsupported FastQ header format: %s"
                                         % seq_header)
        self.format = format

        curr_line = fq_fh.readline().rstrip()
        line_no += 1
        while not curr_line.startswith('+'):
            seq += curr_line
            curr_line = fq_fh.readline().rstrip()
            line_no += 1

        seq_len = len(seq)

        qual_header = curr_line

        curr_line = fq_fh.readline().rstrip()
        while len(qual) < seq_len:
            qual += curr_line
            curr_line = fq_fh.readline().rstrip()
            line_no += 1
            if curr_line == '':
                break
        self.seq_header = seq_header
        self.qual_header = qual_header
        self.seq = seq
        self.qual = qual
        self.file_pos = (line_no_in, line_no)
        self.last_line = curr_line  # as we need to pass this back
        self.name = None
        self.pair_member = None

    def __str__(self):
        # TODO needs to output casava 1.8 format headers
        return "%s\n%s\n%s\n%s" % (self.seq_header, self.seq, self.qual_header, self.qual)

    def validate(self, filename):
        if self.format == FastqFormat.ILLUMINA:
            return self._validate_illumina_format(filename)
        elif self.format == FastqFormat.CASAVA:
            return self._validate_casava_format(filename)

    def _validate_illumina_format(self, filename):
        """
        Checks the record read conforms to expected conventions

        Args:
            filename - filename read was read from, used in error messages

        Raises:
            SeqValidationError - Generic errror with validation
        """
        match = re.match(ILLUMINA_FASTQ_HEADER_PATTERN, self.seq_header)
        if match is None:
            raise SeqValidationError("Sequence record header must match pattern: %s, line %d of %s"
                                     % (ILLUMINA_FASTQ_HEADER_PATTERN, self.file_pos[0], filename))
        groups = match.groups()
        self.name = groups[0]
        self.pair_member = groups[1]

        if len(self.qual) != len(self.seq):
            raise SeqValidationError("Fastq record at line %d of %s appears to be corrupt"
                                     % (self.file_pos[0], filename))

    def _validate_casava_format(self, filename):
        """
        Checks the record read conforms to expected conventions

        Args:
            filename - filename read was read from, used in error messages

        Raises:
            SeqValidationError - Generic errror with validation
        """
        match = re.match(CASAVA_FASTQ_HEADER_PATTERN, self.seq_header)
        if match is None:
            raise SeqValidationError("Sequence record header must match patten: %s, line %d of %s"
                                     % (CASAVA_FASTQ_HEADER_PATTERN, self.file_pos[0], filename))
        groups = match.groups()
        self.name = groups[0] + ' ' + groups[2]
        self.pair_member = groups[1]

        if len(self.qual) != len(self.seq):
            raise SeqValidationError("Fastq record at line %d of %s appears to be corrupt"
                                     % (self.file_pos[0], filename))
