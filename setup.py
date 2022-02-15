from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='pyfracman',
    version='0.1',
    description='A Python toolkit for FracMan',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Scott McKean',
    author_email='scott.mckean@ucalgary.ca',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords=['discrete fracture network', 'fracman', 'geoscience'],
    packages=['pyfracman'],
    python_requires='>=3.9, <4',
    install_requires=[
        'pandas',
        'numpy'
        ],

    project_urls={
        'Fracman': 'https://www.golder.com/fracman/',
    }
)