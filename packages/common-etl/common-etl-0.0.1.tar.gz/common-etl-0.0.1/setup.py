import os

from setuptools import setup, find_packages


# Get the directory where setup.py is located
this_directory = os.path.abspath(os.path.dirname(__file__))

# Read the README.md file
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='common-etl',
    version='0.0.1',
    packages=find_packages(include=['common', 'common.*']),
    install_requires=[],
    author='Kaoushik Kumar',
    author_email='kaoushik.kumar@example.com',
    description='A package for data extraction, transformation, loading, and utilities.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://your-repo-url.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
