#!/usr/bin/env python3

from setuptools import setup

config = {
    'name': 'cgp_seq_input_val',
    'description': 'Code to validate manifests and raw seq data',
    'author': 'Keiran M Raine',
    'url': 'https://gitlab.internal.sanger.ac.uk/CancerIT/cgp_seq_input_val',
    'download_url': 'Where to download it.',
    'author_email': 'cgphelp@sanger.ac.uk',
    'version': '1.1.0',
    'python_requires': '>= 3.3',
    'setup_requires': ['pytest'],
    'install_requires': ['progressbar2', 'xlrd'],
    'packages': ['cgp_seq_input_val'],
    'package_data': {'cgp_seq_input_val': ['config/*.json']},
    'entry_points': {
        'console_scripts': ['cgpSeqInputVal=cgp_seq_input_val.command_line:main'],
    }
}

setup(**config)
