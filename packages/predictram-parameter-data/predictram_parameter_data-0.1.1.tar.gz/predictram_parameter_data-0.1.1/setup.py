# setup.py
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="predictram_parameter_data",
    version="0.1.1",
    author="PredictRAM",
    author_email="support@predictram.com",
    description="A package for querying and analyzing stock parameter data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/predictram-parameter-data",
    packages=find_packages(),
    package_data={
        'predictram_parameter_data': ['data/*.json'],
    },
    install_requires=[
        'pandas>=1.0.0',
        'matplotlib>=3.0.0',
        'seaborn>=0.10.0',
        'openpyxl>=3.0.0',  # For Excel export
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)