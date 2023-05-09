#!/usr/bin/env python
import io
import os
import sys
import setuptools
from setuptools import find_packages, setup, Command
from pathlib import Path
from os.path import dirname

# from tools.clean import CleanCommand

sys.path.append(dirname(__file__))

# setup config.ini if absent
# if not Path("config.ini").is_file():
#     os.system("cp config.ini.dist  config.ini")
# if not Path("download_config.ini").is_file():
#     os.system("cp download_config.ini.dist download_config.ini")

#
# from tools.align import AlignCommand

# from tools.render import RenderCommand
# from tools.download import DownloadCommand
# Package meta-data.
NAME = "fingreen"
DESCRIPTION = "Alignment module of fingreen AI"
URL = "https://github.com/me/myproject"
EMAIL = "francois.amat@fingreen.ai"
AUTHOR = "François Amat"
REQUIRES_PYTHON = ">=3.6.0"
VERSION = "0.1.0"
here = os.path.abspath(os.path.dirname(__file__))


# What packages are required for this module to be executed?

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!


# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

try:
    with open(os.path.join(here, "requirements.txt"), encoding="utf-8") as f:
        REQUIRED = f.readlines()
except FileNotFoundError:
    REQUIRED = []

# What packages are optional?from .cli import cli

EXTRAS = {
    # 'fancy feature': ['django'],
}

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION


setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    # If your package is a single module, use this instead of 'packages':
    # py_modules=['mypackage'],
    # entry_points={
    #     'console_scripts': ['mycli=mymodule:cli'],
    # },
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license="MIT",
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    entry_points={
        "console_scripts": ["finai = cli:cli"],
    },
    # cmdclass={"clean": CleanCommand},
    # $ setup.py publish support.
    # cmdclass={
    #     'align': AlignCommand,
    #     'clean': CleanCommand,
    #     'render': RenderCommand,
    #     'download': DownloadCommand,
    # },
)
