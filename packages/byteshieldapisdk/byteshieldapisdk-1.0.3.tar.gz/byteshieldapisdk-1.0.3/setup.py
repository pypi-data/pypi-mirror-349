import setuptools
from byteshieldapisdk import version

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "byteshieldapisdk",
    version=version,
    author="edgenextapisdk",
    author_email="edgenextapisdk@outlook.com",
    description="Api Sdk For Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/byteshield-cloud/python.api.sdk.v5",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        ##"Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
