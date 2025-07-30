from setuptools import setup, find_packages

setup(
    name="schemaplus-shopify-utils",
    version="0.1.1",
    description="Utility functions for working with the Shopify API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="SchemaPlus",
    author_email="support@schemaplus.io",
    url="https://github.com/uppercasebrands-private/schemaplus-shopify-utils",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)