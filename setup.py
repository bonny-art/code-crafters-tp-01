"""
Setup script for the 'contacts_bot' project.

This script is used to package and distribute the 'contacts_bot' application. 
It reads the required dependencies from the 'requirements.txt' file and configures 
the package for installation using setuptools. The script also sets up an entry point 
for running the bot from the command line.

Attributes:
    current_directory (str): The absolute path of the directory where setup.py is located.
    req_txt_path (str): The absolute path to the 'requirements.txt' file.

Functions:
    read_requirements(): Reads the dependencies from 'requirements.txt' and returns
    them as a list of strings.
"""

import os

from setuptools import setup, find_namespace_packages

# Get the directory where setup.py is located
current_directory = os.path.abspath(os.path.dirname(__file__))
req_txt_path = os.path.join(current_directory, "requirements.txt")

# Read the contents of requirements.txt
def read_requirements():
    """
    Reads the dependencies listed in the 'requirements.txt' file.

    The function opens the 'requirements.txt' file in read mode with UTF-16 encoding,
    reads the contents, and returns them as a list of strings.

    Returns:
        list of str: A list of package dependencies required for the project.
    """
    with open(req_txt_path, 'r', encoding='utf-16') as req_file:
        return req_file.read().splitlines()

setup(
    name='contacts_bot',
    author='code_crafters team',
    version='1.0',
    description="Saving Contacts info",
    url="https://github.com/bonny-art/code-crafters-tp-01",
    packages=find_namespace_packages(),
    py_modules=['main'],
    license="MIT",
    include_package_data=True,
    install_requires=read_requirements(),
    entry_points={
        'console_scripts': [
            'run-bot = main:main',
        ],
    },
)
