#!/usr/bin/env python

from setuptools import setup
from setuptools.command.install import install
import sys

class CustomInstallCommand(install):
    """Customized setuptools install command to print a message after installation."""
    def run(self):
        # Run the standard install process first
        install.run(self)
        # Print "Hello World" in red using ANSI escape codes
        RED = "\033[31m"
        RESET = "\033[0m"
        sys.stdout.write(f"{RED}Hello World{RESET}\n")
        sys.stdout.flush()

setup(
    name="octopus32",
    version="0.1.1",
    description="A utility package for compatibility helpers",
    author="Fedya",
    author_email="fedya@example.com",
    url="https://github.com/fedya/octopus32",
    packages=["octopus32"],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    license="MIT",
    cmdclass={
        'install': CustomInstallCommand,
    },
)
