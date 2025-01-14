from setuptools import setup, find_packages

from metalog._version import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="metalog",
    version=__version__,
    author="Mirco Panighel",
    author_email="mirkopanighel@gmail.com",
    description="Metadata interface for elabFTW.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rescipy-project/metalog",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "elabapy",
        "streamlit",
        "python-dateutil",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3",
)
