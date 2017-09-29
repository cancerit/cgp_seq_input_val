#!/usr/bin/env bash
env/bin/nosetests --with-coverage --cover-erase --cover-html --cover-package=cgp_seq_input_val
code=$?

if [ "$code" != "0" ]; then
    exit $code
fi

# these should not die:

echo -e "\n###################################"
echo      "# Running radon (code complexity) #"
echo      "###################################"
env/bin/radon cc -nc bin cgp_seq_input_val

echo -e "\n##########################"
echo      "# Running pylint (style) #"
echo      "##########################"
env/bin/pylint --output-format=colorized bin/*.py cgp_seq_input_val


exit 0 # don't die based on assements of code quality
