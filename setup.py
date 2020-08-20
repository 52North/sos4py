#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['OWSLib','pandas']

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Alfredo Chavarria Vargas",
    author_email='alchav06@gmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="sos4py is a convenience layer for Python environment to access services from SOS instances.",
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='sos4py',
    name='sos4py',
    packages=find_packages(include=['sos4py', 'sos4py.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/52North/sos4py',
    download_url='https://github.com/52North/sos4py/archive/v0.2.0.tar.gz',
    version='0.2.0',
    zip_safe=False,

)
