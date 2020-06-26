from setuptools import find_packages
from setuptools import setup
import os

this_dir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(this_dir, "README.rst"), "r") as f:
    long_description = f.read()

setup(
    name="flake8-bitbucket",
    description="A flake8 plugin for bitbucket insights.",
    long_description=long_description,
    version="0.1.9",
    author="Alex M.",
    author_email="7845120+newAM@users.noreply.github.com",
    url="https://github.com/newAM/flake8-bitbucket",
    py_modules=["flake8_bitbucket"],
    license="MIT",
    python_requires=">=3.8",
    install_requires=[
        "flake8>=3.8.2",
        "gitpython>=3.1.2",
        "atlassian-python-api>=1.15.7",
    ],
    classifiers=[
        "Environment :: Console",
        "Framework :: Flake8",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
    ],
    entry_points={
        "flake8.report": ["flake8-bitbucket = flake8_bitbucket:Flake8Bitbucket"]
    },
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
)
