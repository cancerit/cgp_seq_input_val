#!/usr/bin/env bash
set -e
pytest --cov-branch --cov-report term --cov-report html --cov=cgp_seq_input_val --cov-fail-under=69 -x
set +e

# these should not die:

echo -e "\n#################################"
echo      "# Running pycodestyle (style)   #"
echo      "#################################"
pycodestyle cgp_seq_input_val

echo -e "\n#########################################"
echo      "# Running radon (cyclomatic complexity) #"
echo      "#########################################"
radon cc -nc cgp_seq_input_val

echo -e "\n#########################################"
echo      "# Running radon (maintainability index) #"
echo      "#########################################"
radon mi -s cgp_seq_input_val

echo -e "\n##############################"
echo      "# Running mdl (markdownlint) #"
echo      "##############################"
mdl .

exit 0 # don't die based on assements of code quality
