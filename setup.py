from __future__ import absolute_import
import setuptools
from setuptools import setup
import os
import sys
_here = os.path.abspath(os.path.dirname(__file__))


from setuptools.command.install import install
from subprocess import check_call

# class PostInstallCommand(install):
#     """Post-installation for installation mode."""
#     def run(self):
#         install.run(self)
#         check_call('llp configure'.split())




with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    requirements = [x.strip() for x in fh.read().split('\n') if x.strip()]

setup(
    name='llp',
    version='0.2.2',
    description=('Literary Language Processing (LLP): corpora, models, and tools for the digital humanities'),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Ryan Heuser',
    author_email='heuser@stanford.edu',
    url='https://github.com/quadrismegistus/llp',
    license='MIT',
    packages=setuptools.find_packages(),
    install_requires=requirements,
    scripts=['bin/llp'],
    include_package_data=True,
    classifiers=[
        #'Development Status :: 3 - Alpha',
        #'Intended Audience :: Science/Research',
        #'Programming Language :: Python :: 2.7',
        #'Programming Language :: Python :: 3.6'
    ],
    # cmdclass={
    #     'install': PostInstallCommand,
    # },

)
