from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
#with open(path.join(here, 'README.md'), encoding='utf-8') as f:
#    long_description = f.read()
setup(
    name='catsHTM',
    version='0.2.5',
    description='Fast access and cross-matching of large astronomical catalogs',
    url='https://github.com/chaorun/catsHTM',

    author='Maayane T. Soumagnac, Eran O. Ofek',
    #author_email='maayane.soumagnac@weizmann.ac.il',
    maintainer='Tianrui Sun',

    license='Apache-2.0',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Astronomy',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Operating System :: OS Independent',
    ],

    keywords='astronomy catalogs cone-search cross-matching HTM HDF5',

    packages=['catsHTM'],

    install_requires=[
        'h5py',
        'scipy',
        'tqdm',
        'hdf5storage',
    ],

    python_requires='>=3.9',

    project_urls={
        'Source': 'https://github.com/chaorun/catsHTM',
        'Bug Reports': 'https://github.com/chaorun/catsHTM/issues',
        'Original Source': 'https://github.com/maayane/catsHTM',
        'Preliminary Documentation': 'https://webhome.weizmann.ac.il/home/eofek/matlab/doc/catsHTM.html',
        'MATLAB Version': 'https://webhome.weizmann.ac.il/home/eofek/matlab/doc/install.html',
        'Credit Page': 'https://webhome.weizmann.ac.il/home/eofek/matlab/doc/catsHTMcredit.html',
    },
)