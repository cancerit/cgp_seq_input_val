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
FileMeta object to handle file actions and conversion from tsv formats
"""

import os
import sys
import gzip  # only used for reading
import bz2  # only used for reading
from xopen import xopen  # only used for writing
import json

# progressbar2
import progressbar

# this package:
from cgp_seq_input_val.error_classes import SeqValidationError
from cgp_seq_input_val.fastq_read import FastqRead, FastqFormat, CasavaFastqRead, IlluminaFastqRead

# From: https://en.wikipedia.org/wiki/FASTQ_format#Encoding
Q_RANGES = {'Sanger': [33, 73],
            'Solexa': [59, 104],
            'Illumina 1.3': [64, 104],
            'Illumina 1.5': [66, 105],  # 2=Read Segment Quality Control Indicator
            'Illumina 1.8': [33, 74]}

PROG_RECORDS = 100000


def validate_seq_files(args):
    """
    Top level entry point for validating sequence files.
    """
    out_fh = None
    try:
        file_2 = None
        if len(args.input) == 2:
            file_2 = args.input[1]
            if args.output:
                out_fh = xopen(args.output, mode='wt')

        validator = SeqValidator(args.input[0], args.qc, out_fh=out_fh, file_b=file_2)
        validator.validate()
        validator.report(args.report)
    except SeqValidationError as ve:  # runtime so no functions for message and errno
        sys.exit("ERROR: " + str(ve))
    # have to catch 2 classes works 3.0-3.3, above 3.3 all IO issues are captured under OSError
    except (OSError, IOError) as err:
        sys.exit("ERROR (%d): %s - %s" % (err.errno, err.strerror, err.filename))
    finally:
        if out_fh:
            out_fh.close()


class SeqValidator(object):
    """
    Validate sequence file, currently only does fastq (interleaved or paired)

    Args:
        file_a - File to be validated (fastq[.gz])
        file_b - optional, second end of pair if paired fastq[.gz]
        progress_pairs - optional, how often to update progress bar [100,000]
                       - set to 0 to disable
    """
    def __init__(self, file_a, qc_reads, file_b=None, out_fh=None, progress_pairs=PROG_RECORDS):
        self.progress_pairs = progress_pairs
        self.qc_reads = qc_reads
        self.file_a = file_a
        self.file_b = file_b
        self.out_fh = out_fh
        self.pairs = 0
        # will use this to decide on path
        self.is_gzip = False  # change open method for fastq
        self.is_bz2 = False  # change open method for fastq
        # sam is not supported

        self.q_min = 1000
        self.q_max = -1
        self.encodings = []
        self.fq_format = None
        self._prep()

    def __str__(self):
        ret = []
        ret.append('file_a: '+self.file_a)
        ret.append('file_b: '+str(self.file_b))
        ret.append('is_gzip: '+str(self.is_gzip))
        ret.append('is_bz2: '+str(self.is_bz2))
        ret.append('q_min: '+str(self.q_min))
        ret.append('q_max: '+str(self.q_max))
        ret.append('encodings: '+str(self.encodings))
        return '\n'.join(ret)

    def _prep(self):
        full_ext = ''
        (base, ext) = os.path.splitext(self.file_a)
        if ext == '.gz':
            self.is_gzip = True
            full_ext = ext
            (base, ext) = os.path.splitext(base)
        elif ext == '.bz2':
            self.is_bz2 = True
            full_ext = ext
            (base, ext) = os.path.splitext(base)

        if ext.lower() not in ('.fastq', '.fq'):
            # This check should be consistent with FastQ file extension restrictions in manifest.py
            raise SeqValidationError("Input files must be fastq|fq[.gz]")

        full_ext = ext + full_ext

        if self.file_b is None:
            self.file_b = self.file_a  # use equality to indicate interleaved
        elif not self.file_b.endswith(full_ext):
            raise SeqValidationError("Input files be of same type")

    def validate(self):
        """
        Trigger the validation of sequence file(s)

        Raises:
            SeqValidationError
        """
        if self.file_a == self.file_b:
            self.validate_interleaved()
        else:
            self.validate_paired()

    def possible_encoding(self):
        """
        Converts the ascii quality score range to something useful for debugging
        """
        for encoding in Q_RANGES:
            if(Q_RANGES[encoding][0] <= self.q_min <= Q_RANGES[encoding][1] and
               Q_RANGES[encoding][0] <= self.q_max <= Q_RANGES[encoding][1]):
                self.encodings.append(encoding)

    def report(self, fp):
        """
        Prints json report to the provided file-pointer

        Args:
            fp - file pointer
        """
        self.possible_encoding()
        report = {'pairs': self.pairs,
                  'valid_q': self.q_min >= 33 and self.q_max <= 74,
                  'interleaved': self.file_a == self.file_b,
                  'possible_encoding': self.encodings,
                  'quality_ascii_range': [self.q_min, self.q_max],
                  'format': self.fq_format.value}
        json.dump(report, fp, sort_keys=True, indent=4)

    def validate_paired(self):
        """
        Validates a paired set of fastq files.

        Raises:
            SeqValidationError
        """
        fq_fh_a = None
        fq_fh_b = None
        file_a = self.file_a
        file_b = self.file_b
        prog_indic = self.progress_pairs
        pairs = 0
        try:
            if self.is_gzip:
                fq_fh_a = gzip.open(self.file_a, 'rt')
                fq_fh_b = gzip.open(self.file_b, 'rt')
            elif self.is_bz2:
                fq_fh_a = bz2.open(self.file_a, 'rt')
                fq_fh_b = bz2.open(self.file_b, 'rt')
            else:
                fq_fh_a = open(self.file_a, 'r')
                fq_fh_b = open(self.file_b, 'r')

            curr_line_a = None
            curr_line_b = None
            fqh_line_a = 0
            fqh_line_b = 0
            bar = self.setup_progress()

            self.fq_format = get_fq_format(fq_fh_a)
            FqClass = None
            if self.fq_format == FastqFormat.ILLUMINA:
                FqClass = IlluminaFastqRead
            else:
                FqClass = CasavaFastqRead

            while True:
                read_1 = FqClass(fq_fh_a, fqh_line_a, curr_line_a)
                read_1.validate(file_a)
                curr_line_a = read_1.last_line
                fqh_line_a = read_1.file_pos[1]

                read_2 = FqClass(fq_fh_b, fqh_line_b, curr_line_b)
                read_2.validate(file_b)
                curr_line_b = read_2.last_line
                fqh_line_b = read_2.file_pos[1]

                self.check_pair(read_1, read_2, self.qc_reads == 0 or pairs < self.qc_reads)

                if self.out_fh:
                    print(read_1, file=self.out_fh)
                    print(read_2, file=self.out_fh)

                pairs += 1

                if bar and pairs % prog_indic == 0:
                    bar.update(pairs/prog_indic)

                if curr_line_a == '':
                    if curr_line_b != '':
                        raise SeqValidationError("Read 1 file finished before read 2")
                    break  # if we get here both files are finished
                if curr_line_b == '':
                    raise SeqValidationError("Read 2 file finished before read 1")
            self.pairs = pairs
        finally:
            print(file=sys.stderr)  # make sure we move to next line when progress finishes
            if fq_fh_a is not None and not fq_fh_a.closed:
                fq_fh_a.close()
            if fq_fh_b is not None and not fq_fh_b.closed:
                fq_fh_b.close()

    def validate_interleaved(self):
        """
        Validates an interleaved fastq file

        Raises:
            SeqValidationError
        """
        prog_indic = self.progress_pairs
        fq_fh = None
        file_a = self.file_a
        try:
            if self.is_gzip:
                fq_fh = gzip.open(self.file_a, 'rt')
            elif self.is_bz2:
                fq_fh = bz2.open(self.file_a, 'rt')
            else:
                fq_fh = open(self.file_a, 'r')

            curr_line = None
            fqh_line = 0
            bar = self.setup_progress()
            pairs = 0

            self.fq_format = get_fq_format(fq_fh)
            FqClass = None
            if self.fq_format == FastqFormat.ILLUMINA:
                FqClass = IlluminaFastqRead
            else:
                FqClass = CasavaFastqRead

            while True:
                read_1 = FqClass(fq_fh, fqh_line, curr_line)
                read_1.validate(file_a)
                curr_line = read_1.last_line

                read_2 = FqClass(fq_fh, read_1.file_pos[1], curr_line)
                read_2.validate(file_a)
                curr_line = read_2.last_line

                # ensure line increments based on the last line read
                fqh_line = read_2.file_pos[1]

                self.check_pair(read_1, read_2, self.qc_reads == 0 or pairs < self.qc_reads)
                pairs += 1

                if bar and pairs % prog_indic == 0:
                    bar.update(pairs/prog_indic)

                if curr_line == '':
                    break
            self.pairs = pairs
        finally:
            print(file=sys.stderr)  # make sure we move to next line when progress finishes
            if fq_fh is not None and not fq_fh.closed:
                fq_fh.close()

    def qual_range(self, read):
        """
        Finds the min and max ascii values from each quality encoding
        """
        sorted_qual = list(map(ord, read.qual))
        sorted_qual.sort()  # faster than sorted(list(...))
        if self.q_min > sorted_qual[0]:
            self.q_min = sorted_qual[0]

        if self.q_max < sorted_qual[-1]:
            self.q_max = sorted_qual[-1]

    def check_pair(self, read_1, read_2, check_qual):
        """
        Compares a pair of reads

        Raises:
            SeqValidationError
        """
        if check_qual:
            self.qual_range(read_1)
            self.qual_range(read_2)

        if read_1.name != read_2.name:
            raise SeqValidationError("Fastq record name at line %d should be a \
                                     match to paired file line %s:\
                                     \n\t%s (%s)\n\t%s (%s)"
                                     % (read_1.file_pos[0], read_2.file_pos[0],
                                        read_1.name, self.file_a,
                                        read_2.name, self.file_b))
        if read_1.pair_member != '1':
            raise SeqValidationError("Fastq record at line %d of %s should be \
                                     for first in pair, got '%s'"
                                     % (read_1.file_pos[0], self.file_a, read_1.pair_member))

        if read_2.pair_member != '2':
            raise SeqValidationError("Fastq record at line %d of %s should be \
                                     for second in pair, got '%s'"
                                     % (read_2.file_pos[0], self.file_b, read_2.pair_member))

    def setup_progress(self):
        """
        Sets up the progress indicator and indicate units
        """
        if self.progress_pairs == 0:
            return None
        bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
        print("Progress is %d's of record pairs" % (self.progress_pairs), file=sys.stderr)
        bar.update(0)
        return bar


def get_fq_format(file_h):
    read = FastqRead(file_h, 0, None)
    file_h.seek(0)  # reset file pointer to the begaining
    return read.get_fq_format()
