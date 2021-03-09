########## LICENCE ##########
# Copyright (c) 2017-2019 Genome Research Ltd.
#
# Author: CASM/Cancer IT <cgphelp@sanger.ac.uk>
#
# This file is part of cgp_seq_input_val.
#
# cgp_seq_input_val is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation; either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
# details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# 1. The usage of a range of years within a copyright statement contained within
# this distribution should be interpreted as being equivalent to a list of years
# including the first and last year specified and all consecutive years between
# them. For example, a copyright statement that reads ‘Copyright (c) 2005, 2007-
# 2009, 2011-2012’ should be interpreted as being identical to a statement that
# reads ‘Copyright (c) 2005, 2007, 2008, 2009, 2011, 2012’ and a copyright
# statement that reads ‘Copyright (c) 2005-2012’ should be interpreted as being
# identical to a statement that reads ‘Copyright (c) 2005, 2006, 2007, 2008,
# 2009, 2010, 2011, 2012’."
########## LICENCE ##########

"""
Models a fastq read
"""

import re
from enum import Enum
from cgp_seq_input_val.error_classes import SeqValidationError

ILLUMINA_FASTQ_HEADER_PATTERN = re.compile(r'^@(\S+)/([12])$')
CASAVA_FASTQ_HEADER_PATTERN = re.compile(r'^@(\S+)\s([12])(:[YN]+:[\d+]+:\S+)$')


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
    def __init__(self, fq_fh, line_no_in, curr_line):
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
        return "%s\n%s\n%s\n%s" % (self.seq_header, self.seq, self.qual_header, self.qual)

    def get_fq_format(self):
        if ILLUMINA_FASTQ_HEADER_PATTERN.match(self.seq_header) is not None:
            format = FastqFormat.ILLUMINA
        elif CASAVA_FASTQ_HEADER_PATTERN.match(self.seq_header) is not None:
            format = FastqFormat.CASAVA
        else:
            raise SeqValidationError("Unsupported FastQ header format: %s"
                                     % self.seq_header)
        return format


class CasavaFastqRead(FastqRead):

    def validate(self, filename):
        """
        Checks the record read conforms to expected conventions

        Args:
            filename - filename read was read from, used in error messages

        Raises:
            SeqValidationError - Generic errror with validation
        """
        match = CASAVA_FASTQ_HEADER_PATTERN.match(self.seq_header)
        if match is None:
            raise SeqValidationError(
                "Sequence record header must match pattern: '%s', line %d of %s"
                % (CASAVA_FASTQ_HEADER_PATTERN.pattern, self.file_pos[0], filename))
        groups = match.groups()
        self.name = groups[0] + ' ' + groups[2]
        self.pair_member = groups[1]

        if len(self.qual) != len(self.seq):
            raise SeqValidationError("Fastq record at line %d of %s appears to be corrupt"
                                     % (self.file_pos[0], filename))


class IlluminaFastqRead(FastqRead):

    def validate(self, filename):
        """
        Checks the record read conforms to expected conventions

        Args:
            filename - filename read was read from, used in error messages

        Raises:
            SeqValidationError - Generic errror with validation
        """
        match = ILLUMINA_FASTQ_HEADER_PATTERN.match(self.seq_header)
        if match is None:
            raise SeqValidationError(
                "Sequence record header must match pattern: '%s', line %d of %s"
                % (ILLUMINA_FASTQ_HEADER_PATTERN.pattern, self.file_pos[0], filename))
        groups = match.groups()
        self.name = groups[0]
        self.pair_member = groups[1]

        if len(self.qual) != len(self.seq):
            raise SeqValidationError("Fastq record at line %d of %s appears to be corrupt"
                                     % (self.file_pos[0], filename))
