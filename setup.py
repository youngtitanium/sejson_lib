from setuptools import setup

import sejson

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='sejson',
    version=sejson.__version__,
    packages=['sejson'],
    url='https://github.com/yungtitanium/sejson',
    license='MIT License',
    author='YoungTitanium',
    python_requires='>=3.8.1',
    description='Easily edit the JSON files',
    long_description=long_description,
    long_description_content_type="text/html",
)
