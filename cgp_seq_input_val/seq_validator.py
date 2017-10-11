"""
FileMeta object to handle file actions and conversion from tsv formats
"""

import os
import sys
import gzip
import json

# progressbar2
import progressbar

# this package:
from cgp_seq_input_val.error_classes import SeqValidationError
from cgp_seq_input_val.fastq_read import FastqRead

prog_records = 100000

def validate_seq_files(args):
    """
    Top level entry point for validating sequence files.
    """
    try:
        file_2 = None
        if len(args.input) == 2:
            file_2 = args.input[1]
        validator = SeqValidator(args.input[0], file_2)
        validator.validate()
        validator.report(args.report)
    except SeqValidationError as ve:  # runtime so no functions for message and errno
        sys.exit("ERROR: " + str(ve))
    # have to catch 2 classes works 3.0-3.3, above 3.3 all IO issues are captured under OSError
    except (OSError, IOError) as err:
        sys.exit("ERROR (%d): %s - %s" % (err.errno, err.strerror, err.filename))


class SeqValidator(object):
    """
    Validate sequence file, currently only does fastq (interleaved or paired)

    Args:
        file_a - File to be validated (fastq[.gz])
        file_b - optional, second end of pair if paired fastq[.gz]
        progress_pairs - optional, how often to update progress bar [100,000]
                       - set to 0 to disable
    """
    def __init__(self, file_a, file_b=None, progress_pairs=prog_records):
        self.progress_pairs = progress_pairs
        self.file_a = file_a
        self.file_b = file_b
        self.pairs = 0
        # will use this to decide on path
        self.is_gzip = False  # change open method for fastq
        # sam is not supported

        # only the min value is actually needed to determine if scaling
        # is Sanger or Illumina 1.8+
        self.q_min = 1000
        self._prep()

    def __str__(self):
        ret = []
        ret.append('file_a: '+self.file_a)
        ret.append('file_b: '+str(self.file_b))
        ret.append('is_gzip: '+str(self.is_gzip))
        ret.append('q_min: '+str(self.q_min))
        return '\n'.join(ret)

    def _prep(self):
        full_ext = ''
        (base, ext) = os.path.splitext(self.file_a)
        if ext == '.gz':
            self.is_gzip = True
            full_ext = ext
            (base, ext) = os.path.splitext(base)

        if ext not in ('.fastq', '.fq'):
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

    def report(self, fp):
        """
        Prints json report to the provided file-pointer

        Args:
            fp - file pointer
        """
        report = {'pairs': self.pairs,
                  'valid_q': self.q_min == 33,
                  'interleaved': self.file_a == self.file_b}
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
            else:
                fq_fh_a = open(self.file_a, 'r')
                fq_fh_b = open(self.file_b, 'r')

            curr_line_a = None
            curr_line_b = None
            fqh_line_a = 0
            fqh_line_b = 0
            bar = self.setup_progress()
            while True:
                read_1 = FastqRead(fq_fh_a, fqh_line_a, curr_line_a)
                read_1.validate(file_a)
                curr_line_a = read_1.last_line
                fqh_line_a = read_1.file_pos[1]

                read_2 = FastqRead(fq_fh_b, fqh_line_b, curr_line_b)
                read_2.validate(file_b)
                curr_line_b = read_2.last_line
                fqh_line_b = read_2.file_pos[1]

                self.check_pair(read_1, read_2)
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
            else:
                fq_fh = open(self.file_a, 'r')

            curr_line = None
            fqh_line = 0
            bar = self.setup_progress()
            pairs = 0
            while True:
                read_1 = FastqRead(fq_fh, fqh_line, curr_line)
                read_1.validate(file_a)
                curr_line = read_1.last_line

                read_2 = FastqRead(fq_fh, read_1.file_pos[1], curr_line)
                read_2.validate(file_a)
                curr_line = read_2.last_line

                # ensure line increments based on the last line read
                fqh_line = read_2.file_pos[1]

                self.check_pair(read_1, read_2)
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

    def check_pair(self, read_1, read_2):
        """
        Compares a pair of reads

        Raises:
            SeqValidationError
        """
        if self.q_min > 33:
            # once a min of 33 is achieved it must be sanger/Illumina 1.8+
            # may need occasional review.
            q_min = min(map(ord, read_1.qual))
            if self.q_min > q_min:
                self.q_min = q_min

        if read_1.name != read_2.name:
            raise SeqValidationError("Fastq record name at line %d should be a match to paired file line %s:\
                                     \n\t%s (%s)\n\t%s (%s)"
                                     % (read_1.file_pos[0], read_2.file_pos[0],
                                        read_1.name, self.file_a,
                                        read_2.name, self.file_b))
        if read_1.end != '1':
            raise SeqValidationError("Fastq record at line %d of %s should be for first in pair, got '%s'"
                                     % (read_1.file_pos[0], self.file_a, read_1.end))

        if read_2.end != '2':
            raise SeqValidationError("Fastq record at line %d of %s should be for second in pair, got '%s'"
                                     % (read_2.file_pos[0], self.file_b, read_2.end))

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
