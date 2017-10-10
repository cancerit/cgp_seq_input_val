#!/usr/bin/env bash
set -e
env/bin/nosetests --with-coverage --cover-erase --cover-html --cover-min-percentage=50 --cover-package=cgp_seq_input_val
set +e

# these should not die:

echo -e "\n##########################"
echo      "# Running pylint (style) #"
echo      "##########################"
env/bin/pylint --output-format=colorized bin/*.py cgp_seq_input_val

echo -e "\n#########################################"
echo      "# Running radon (cyclomatic complexity) #"
echo      "#########################################"
env/bin/radon cc -nc bin cgp_seq_input_val

echo -e "\n#########################################"
echo      "# Running radon (maintainability index) #"
echo      "#########################################"
env/bin/radon mi -s -n B bin cgp_seq_input_val

exit 0 # don't die based on assements of code quality
