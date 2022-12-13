import os
import platform
import sys

from codecs import open as codecs_open
from setuptools import setup, find_packages  # type: ignore

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

about = {}  # type: ignore
here = os.path.abspath(os.path.dirname(__file__))
with codecs_open(os.path.join(here, "macrobond_data_api", "__version__.py"), "r", "utf-8") as f:
    exec(f.read(), about)  # pylint: disable=exec-used

setup(
    name="macrobond-data-api",
    packages=find_packages(include=["macrobond_data_api", "macrobond_data_api.*"]),
    version=about["__version__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    description=about["__description__"],
    # long_description=attr.__long_description__,
    url=about["__url__"],
    # keywords="sample, example, setuptools",
    # https://pypi.org/classifiers/
    classifiers=[
        "License :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    python_requires=">=3.7",
    install_requires=install_requires,
    extras_require={"dev": dev_require, "socks": ["requests[socks]>=" + REQUESTS_VERSION]},
)
