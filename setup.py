#!/usr/bin/env python
import os
from setuptools import setup, find_packages, Command
from setuptools.command.build_py import build_py

from hfcommon import version


def find_package_data(package, *directories):
    data_files = []
    current_dir = os.path.abspath(os.curdir)
    package_dir = os.path.dirname(__import__(package, fromlist=[""]).__file__)
    os.chdir(package_dir)

    for directory in directories:
        for dirpath, dirnames, filenames in os.walk(directory):
            [data_files.append(os.path.join(dirpath, f)) for f in filenames]

    os.chdir(current_dir)

    return data_files


class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import nose
        nose.main(argv=['nosetests', 'hfcommon_tests/'])


class BuildHook(build_py):
    def run(self):
        build_py.run(self)

        build_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.build_lib, 'hfcommon')
        with open(os.path.join(build_dir, 'version.py'), 'w') as version_file:
            version_file.write('version = "{0}"\n'.format(version))


install_requires = ['phonenumbers', 'arrow', 'python-dateutil', 'six', 'tortik']

setup(
    name="hfcommon",
    version=version,
    description="Huntflow Common Library",
    long_description=open("README.rst").read(),
    url="https://github.com/glibin/huntflow",
    download_url='https://github.com/glibin/huntflow/tarball/{}'.format(version),
    packages=find_packages(exclude=['hfcommon_tests', 'hfcommon_tests.*']),
    package_data={

    },
    cmdclass={'test': TestCommand, 'build_py': BuildHook},
    install_requires=install_requires,
    setup_requires=['nose', 'pycodestyle'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
