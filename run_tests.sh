#!/usr/bin/env bash
env/bin/nosetests --with-coverage --cover-erase --cover-html --cover-package=cgp_seq_input_val
code=$?

if [ "$code" != "0" ]; then
    exit $code
fi

echo -e "\n#################\n# Running pylint:\n"
env/bin/pylint --output-format=colorized bin/*.py cgp_seq_input_val
echo -e "#\n#################"
exit 0 # don't die based on pylint
