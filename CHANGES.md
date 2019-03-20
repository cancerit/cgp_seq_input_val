# CHANGES

## 1.5.3

* `+` is not allowed in file names anymore, as CWL could not "glob" an output with a `+` in its name

## 1.5.2

* Reject files in a manifest with characters that not compatible with CWL file name restrictions in their names.
  * This is can be disabled by setting `reject_cwl_incompatible_filename` to false in config file.
  * CWLtool uses [this pattern][cwl-filename-restriction] to validate file names.

## 1.5.1

* White spaces around any cell in a manifest is removed before converting and validating it.

## 1.5.0

* IMPORT 1.0 changed to merge Seq Protocol and Data Type
* Compitable with FastQs in CASAVA 1.8 format

## 1.4.2

* added function to process `bz2` compressed FastQ format.

## 1.4.1

* `validator` now allows upper case in FastQ file name extensions

## 1.4.0

* Correct base config for file types accepted.  File_2 should only accept `f(?:ast)q.gz` (upper/lower)
* Only allow compresed fastq.

## 1.3.0

* Fixes `valid_q` value of `seq-valid` json report.  Always returned false previously.
* Correct command line help text for `seq-valid` input option.
* Extends the `seq-valid` json report to include the ascii range detected and which types of phred
  score these align to.
* Additional command line options for `seq-valid`
  * `-o | --output` - Generates an interleaved gzip compressed fastq file when input is paired fastq
  * `-q | --qc` - Specify the number of pairs to be used when assessing the phred quality range
    * Added for performance reasons

## 1.2.1

* More informative exceptions for low-level issues

## 1.2.0

* Changes to command line, using sub commands now
* Changed test framework
* Add travis and codeclimate checks

## 1.1.0

* Fixed issue of `json.loads()` in py<3.5 being unable to decode resource string to utf-8 automatically.
* Adds a UUID to the header of a processed manifest if incoming not set
* Improve documentation

## 1.0.0

Early functional release

<!-- References -->

[cwl-filename-restriction]: https://github.com/common-workflow-language/cwltool/blob/8f896370b043dc9c6802521550210ce1bad1cfd8/cwltool/command_line_tool.py#L58
