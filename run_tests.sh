#!/usr/bin/env bash
set -e
pytest --cov-report term --cov-report html --cov=cgp_seq_input_val --cov-fail-under=50
set +e

# these should not die:

echo -e "\n##########################"
echo      "# Running pylint (style) #"
echo      "##########################"
pylint --output-format=colorized cgp_seq_input_val

echo -e "\n#########################################"
echo      "# Running radon (cyclomatic complexity) #"
echo      "#########################################"
radon cc -nc cgp_seq_input_val

echo -e "\n#########################################"
echo      "# Running radon (maintainability index) #"
echo      "#########################################"
radon mi -s -n B cgp_seq_input_val

exit 0 # don't die based on assements of code quality
