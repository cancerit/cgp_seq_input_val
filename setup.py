from setuptools import setup

config = {
    'name': 'cgp_seq_input_val',
    'description': 'Code to validate manifests and raw seq data',
    'author': 'Keiran M Raine',
    'url': 'URL to get it at.',
    'download_url': 'Where to download it.',
    'author_email': 'cgphelp@sanger.ac.uk',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['cgp_seq_input_val'],
    'scripts': []
}

setup(**config)
