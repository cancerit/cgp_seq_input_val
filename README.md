# cgp_seq_input_val_tests

This package is contains tools to validate manifests and validate various types
of sequence data file commonly used for NGS data.

## Design

Many components of this system are heavily driven by configuration files.  This
is to allow new validation code to be added and incorporated without modifying
the driver code.


# INSTALL

## Dependencies

pip3 install xlrd


# Development environment

After clone cd into the project and run:

```
git config core.hooksPath git-hooks
```

## Dependencies

* python3
* nosetests-3+ (exported as `NOSETESTS3`)
* coverage
* pylint

```
pip3 install nosetests
pip3 install coverage
pip3 install pylint
```
