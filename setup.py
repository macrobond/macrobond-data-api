import os
import platform
import sys

from codecs import open as codecs_open
from setuptools import setup, find_packages  # type: ignore

extras_require = [
    "mypy",
    "pylint",
    "pycodestyle",
    "pdoc3",
    "build",
    "coverage",
    "black[jupyter]",
]

install_requires = ["keyring", "Authlib", "requests", "python-dateutil", "ijson"]

if platform.python_implementation() != "PyPy":
    for extra in ["matplotlib", "statsmodels", "scikit-learn", "pandas"]:
        extras_require.append(extra)

    if sys.platform == "win32":
        install_requires.append("pywin32")

about = {}  # type: ignore
here = os.path.abspath(os.path.dirname(__file__))
with codecs_open(os.path.join(here, "macrobond_financial", "__version__.py"), "r", "utf-8") as f:
    exec(f.read(), about)  # pylint: disable=exec-used

setup(
    name="macrobond_financial",
    packages=find_packages(include=["macrobond_financial", "macrobond_financial.*"]),
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
    extras_require={
        "dev": extras_require,
    },
)
