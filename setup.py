import os
import platform
import sys
import subprocess

from setuptools import setup, find_packages  # type: ignore

AUTHOR = "Macrobond Financial"
AUTHOR_EMAIL = "support@macrobond.com"
DESCRIPTION = "Exposes a common API in Python for the Macrobobond Web and Client Data APIs"
LICENSE = "MIT License"
URL = "https://github.com/macrobond/macrobond-data-api"

with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

try:
    version = (
        subprocess.run(["git", "describe", "--tags"], stdout=subprocess.PIPE, check=True)
        .stdout.decode("utf-8")
        .strip()
    )
    print("using tag")
except subprocess.CalledProcessError:
    FOLDER_NAME = os.path.basename(os.getcwd())
    if FOLDER_NAME.startswith("macrobond-data-api-"):
        START_INDEX = len("macrobond-data-api-")
        version = FOLDER_NAME[START_INDEX:]
        print("using dir name")
    else:
        print("no tag or dir name using default")
        version = "0.0.0"  # pylint: disable=invalid-name

if "-" in version:
    v, i, s = version.split("-")
    version = v + "+" + i + ".git." + s

print("version: " + version)

assert "-" not in version
assert "." in version

# fmt: off
PACKAGE_INFO = '''# -*- coding: utf-8 -*-

__version__ = "''' + version + '''"
__author__ = "''' + AUTHOR + '''"
__author_email__ = "''' + AUTHOR_EMAIL + '''"
__description__ = "''' + DESCRIPTION + '''"
__license__ = "''' + LICENSE + '''"
__url__ = "''' + URL + '''"
'''
# fmt: on

with open(os.path.join("macrobond_data_api", "__version__.py"), "w+", encoding="utf-8") as fh:
    fh.write(PACKAGE_INFO)

REQUESTS_VERSION = "2.28.1"

dev_require = [
    "mypy>=0.991",
    "pylint>=2.15.8",
    "pycodestyle>=2.10.0",
    "pdoc3>=0.10.0",
    "build>=0.9.0",
    "coverage>=6.5.0",
    "black[jupyter]>=22.12.0",
    "requests[socks]>=" + REQUESTS_VERSION,
]

install_requires = [
    "keyring>=23.11.0",
    "Authlib>=1.2.0",
    "requests>=" + REQUESTS_VERSION,
    "python-dateutil>=2.8.2",
    "ijson>=3.1.4",
]

if platform.python_implementation() != "PyPy":
    for extra in ["matplotlib", "statsmodels", "scikit-learn", "pandas"]:
        dev_require.append(extra)

    if sys.platform == "win32":
        install_requires.append("pywin32>=305")

setup(
    name="macrobond-data-api",
    packages=find_packages(include=["macrobond_data_api", "macrobond_data_api.*"]),
    version=version,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url=URL,
    # TODO @mb-jp add keywords
    # keywords="sample, example, setuptools",
    # https://pypi.org/classifiers/
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    python_requires=">=3.7",
    install_requires=install_requires,
    extras_require={"dev": dev_require, "socks": ["requests[socks]>=" + REQUESTS_VERSION]},
    project_urls={
        "Documentation": "https://macrobond.github.io/macrobond-data-api",
        "Source": "https://github.com/macrobond/macrobond-data-api",
    },
)
