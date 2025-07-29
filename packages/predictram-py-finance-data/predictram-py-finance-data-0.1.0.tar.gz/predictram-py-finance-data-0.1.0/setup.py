from setuptools import setup, find_packages

setup(
    name="predictram-py-finance-data",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pandas>=1.0.0',
        'openpyxl>=3.0.0',
        'matplotlib>=3.0.0',
        'seaborn>=0.11.0',
        'numpy>=1.0.0',
    ],
    author="Predictram",
    author_email="support@predictram.com",
    description="A Python library for querying and analyzing financial stock data with natural language processing",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/predictram/predictram-py-finance-data",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)