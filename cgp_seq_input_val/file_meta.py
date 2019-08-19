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


class FileMeta(object):
    """
    Oject to hold file metadata as a set of attributes with small set of
    functions to validate actual files.
    """
    def __init__(self, headers, details, rel_path):
        self.attributes = {}
        self.rel_path = rel_path
        cnt = 0
        for h in headers:
            val = None
            if cnt == len(details) and h == 'File_2':
                val = '.'
            else:
                val = details[cnt]

            self.attributes[h] = val
            cnt += 1

    def get_path(self, f_type):
        """
        Returns the path of a file after pre-pending with the 'rel_path'
        All file entries in the manifest should be relative to the manifest
        itself.
        """
        item = self.attributes[f_type]
        if item == '.':
            return None
        return os.path.join(self.rel_path, item)

    def test_files(self, line):
        """
        Checks file exist and are not empty
        """
        for f_type in ('File', 'File_2'):
            item = self.attributes[f_type]
            full_path = self.get_path(f_type)
            # File one controlled by config.json
            if full_path is None and f_type == 'File_2':
                continue

            if not os.path.isfile(full_path):
                raise FileValidationError("'%s' is not a file ('%s' - line %d)."
                                          % (item, f_type, line))
            if not os.path.getsize(full_path):
                raise FileValidationError("'%s' is an empty file ('%s' - line %d)."
                                          % (item, f_type, line))


class FileValidationError(RuntimeError):
    """
    Exception for failures to validate data in the manifest.
    """
    pass
