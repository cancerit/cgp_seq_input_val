import os, json, re, sys, stat, shutil
from importlib import import_module

from pprint import pprint

from cgp_seq_input_val import constants

def normalise(args):
    # ALTERNATE SUCCESS PATHS in this block
    # Extensions are checked by argparse
    if args.input.endswith('tsv') == True:
        if args.output is None:
            print("\nINFO: input and output will be same file, no action required\n", file=sys.stderr)
            return True
        else:
            if os.path.exists(args.output):
                # test if in/out file are the same, inode is simpler to test than stingified paths
                if_node = os.stat(args.input)[stat.ST_INO]
                of_node = os.stat(args.output)[stat.ST_INO]
                if if_node == of_node:
                    print("\nINFO: input and output point to the same file, no action required", file=sys.stderr)
                    return True
            # anything else is a copy
            print("\nINFO: input copied to output, no format conversion required.", file=sys.stderr)
            shutil.copyfile(args.input, args.output, follow_symlinks=True)
            return True

    if ( args.input.endswith('tsv') == False and args.output is None ):
        args.output = re.sub(r'\.[^.]+$', '.tsv', args.input)

    manifest = Manifest(args.input)
    manifest.convert_by_extn(args.output)

class Manifest(object):
    def __init__(self, infile):
        self.infile = infile
        self.informat = os.path.splitext(infile)[1][1:]

    def _xlsx_to_tsv(self, ofh):
        self._excel_to_tsv(ofh)

    def _xls_to_tsv(self, ofh):
        self._excel_to_tsv(ofh)

    def _csv_to_tsv(self, ofh):
        csv = import_module('csv')
        with open(self.infile, 'r') as csvfh:
            for row in csv.reader(csvfh, delimiter=','):
                joined = "\t".join(row)
                if not joined.startswith('\t'):
                    print(joined, file=ofh)

    def _excel_to_tsv(self, ofh):
        xlrd = import_module('xlrd')
        book = xlrd.open_workbook(self.infile, formatting_info=False, on_demand=True, ragged_rows=True )
        sheet = book.sheet_by_name('For entry')
        for r in range(0,sheet.nrows):
            simplerow = []
            cols = sheet.row_len(r)
            # do some cleanup
            if (cols == 0 or sheet.cell_value(r,0) == ''): continue
            for c in range(0,cols):
                simplerow.append(str(sheet.cell_value(r,c)))
            print("\t".join(simplerow), file=ofh)

    def convert_by_extn(self, outfile):
        """Uses the input file extension to determine the correct file conversion
        routine.  Output is always tsv file.  Expects the output file name extension
        to have been checked in advance.
        """
        with open(outfile, 'w') as ofh:
            convertor = getattr(self, '_' + self.informat + '_to_tsv')
            convertor(ofh)

    def validate(self):
        if self.informat != 'tsv':
            raise ValueError('Manifest.validate only accepts files of type "tsv"')
        # Generate the header object
        self.header = Header(self.infile)
        self.config = self.header.get_config()
        self.header.validate(self.config['header'])


class Header(object):
    def __init__(self, manifest):
        self.manifest = manifest
        csv = import_module('csv')
        header_items = {}
        with open(self.manifest, 'r') as ifh:
            for row in csv.reader(ifh, delimiter='\t'):
                if row[0] == constants.HEADER_BODY_SWITCH:
                    break
                val = ''
                if(len(row) > 1):
                    val = row[1]
                header_items[row[0]] = val

        # now load the ini based on 'Form type:' and 'Form version:'
        self.type = header_items['Form type:']
        self.version = header_items['Form version:']
        self._all_items = header_items
        self.items = {}

    def get_config(self):
        """
        Return the location of the config file to use in validation steps
        """
        cfg_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                            'config',
                            '%s-%s.json' % (self.type, self.version))
        with open(cfg_file, 'r') as j:
            config = json.load(j)

        if config['type'] != self.type:
            raise ParsingError("Filename (%s) does not match 'type' (%s) within file" % (cfg_file, config['type']))
        if config['version'] != self.version:
            raise ParsingError("Filename (%s) does not match 'version' (%s) within file" % (cfg_file, config['version']))

        self.validate_json(config)
        return config

    def validate_json(self, config):
        """
        Check the config is valid, simple set of rules:
        1. 'header' exists:
          - 'expected', 'required' and 'validate' must exist.
          - 'validate' keys must exist in 'required' list.
          - 'required' list must exist in 'expected' list.
        2. 'body' exists:
          - body content validated by it's own class.
        """
        if 'header' not in config:
            raise ConfigError("header (dict/hash) not found in json file: %s-%s.json" % (self.type, self.version))
        if 'expected' not in config['header']:
            raise ConfigError("header.expected (list/array) not found in json file: %s-%s.json" % (self.type, self.version))
        if 'required' not in config['header']:
            raise ConfigError("header.required (list/array) not found in json file: %s-%s.json" % (self.type, self.version))
        if 'validate' not in config['header']:
            raise ConfigError("header.validate (dict/hash) not found in json file: %s-%s.json" % (self.type, self.version))
        if 'body' not in config:
            raise ConfigError("body (dict/hash) not found in json file: %s-%s.json" % (self.type, self.version))

    def fields_exist(self, expected):
        """
        Checks all field that are expected to exist in the header of this type+version
        of the manifest.  It is not checking for values, just the expected elements.
        These are detailed in the header.expected element of the json file.
        Adds these to the 'items' dict of the header object.
        """
        found = set(self._all_items.keys())
        expected_fields = set(expected)
        unexpected = found.difference(expected_fields)
        if len(unexpected) > 0:
            raise ValidationError("The following unexpected fields were found in the header of your file:\n\t'" + "'\n\t'".join(unexpected) + "'")
        missing_fields = expected_fields.difference(found)
        if len(missing_fields) > 0:
            raise ValidationError("The following expected fields were missing from the header of your file:\n\t'" + "'\n\t'".join(missing_fields) + "'")
        # add the elements to the approved header items dict
        for key, val in self._all_items.items():
            if key in ('Form type:', 'Form version:'): continue
            self.items[key]=val

    def fields_have_values(self, required):
        """
        Check all fields that should have values do for this type+version.
        These are detailed in the header.required element of the json file.
        """
        for item in required:
            if len(self.items[item]) == 0:
                raise ValidationError("Header item '%s' has no value." % (item) )

    def field_values_valid(self, validate):
        """
        Checks all restricted fields have valid values for this type+version.
        """
        for item in validate:
            if self.items[item] not in validate[item]:
                raise ValidationError("Header item '%s' has an invalid value of: %s" % (item,  self.items[item]) )



    def validate(self, rules):
        self.fields_exist(rules['expected'])
        self.fields_have_values(rules['required'])
        self.field_values_valid(rules['validate'])

class ConfigError(RuntimeError):
    pass

class ParsingError(RuntimeError):
    pass

class ValidationError(RuntimeError):
    pass
