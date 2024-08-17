from setuptools import setup, find_namespace_packages
import os

# Get the directory where setup.py is located
current_directory = os.path.abspath(os.path.dirname(__file__))
req_txt_path = os.path.join(current_directory, "requirements.txt")

# Read the contents of requirements.txt
def read_requirements():
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
