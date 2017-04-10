import os
import xlrd,csv

class Manifest(object):
    def __init__(self, infile):
        self.infile = infile
        self.informat = os.path.splitext(infile)[1][1:]

    def _xlsx_to_tsv(self, ofh):
        self._excel_to_tsv(ofh)

    def _xls_to_tsv(self, ofh):
        self._excel_to_tsv(ofh)

    def _csv_to_tsv(self, ofh):
        with open(self.infile, 'r') as csvfh:
            for row in csv.reader(csvfh, delimiter=','):
                joined = "\t".join(row)
                if joined.replace('\t','') != '':
                    print(joined, file=ofh)
        csvfh.closed

    def _excel_to_tsv(self, ofh):
        book = xlrd.open_workbook(self.infile, formatting_info=False, on_demand=True, ragged_rows=True )
        sheet = book.sheet_by_name('For entry')
        for r in range(0,sheet.nrows):
            simplerow = []
            cols = sheet.row_len(r)
            # do some cleanup
            if (cols == 0 or (cols == 2 and sheet.cell_value(r,0) == '')): continue
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
        ofh.closed
