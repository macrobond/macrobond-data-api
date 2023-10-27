import os
import subprocess
import setuptools

version_info_path = os.path.join("macrobond_data_api", "__version__.py")

AUTHOR = "Macrobond Financial"
AUTHOR_EMAIL = "support@macrobond.com"
DESCRIPTION = "Exposes a common API in Python for the Macrobond Web and Client Data APIs"
LICENSE = "MIT License"
URL = "https://github.com/macrobond/macrobond-data-api"

with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

try:
    version = (
        subprocess.run(["git", "describe", "--tags"], stdout=subprocess.PIPE, check=True).stdout.decode("utf-8").strip()
    )
    if version[0].lower() == "v":
        version = version[1:]
    print("version is from git tag")
except subprocess.CalledProcessError:
    if os.path.exists(version_info_path):
        with open(version_info_path, "r", encoding="utf-8") as f:
            about: dict = {}
            exec(f.read(), about)  # pylint: disable=exec-used
            version = about["__version__"]
            print("version is from " + version_info_path)
    else:
        version = "0.0.0"  # pylint: disable=invalid-name
        print("version is default")

if "-" in version:
    v, i, s = version.split("-")
    version = v + "+" + i + ".git." + s

print("version: " + version)

assert "-" not in version
assert "." in version

# fmt: off
PACKAGE_INFO = '''

__version__ = "''' + version + '''"
__author__ = "''' + AUTHOR + '''"
__author_email__ = "''' + AUTHOR_EMAIL + '''"
__description__ = "''' + DESCRIPTION + '''"
__license__ = "''' + LICENSE + '''"
__url__ = "''' + URL + '''"
'''
# fmt: on

with open(version_info_path, "w+", encoding="utf-8") as fh:
    fh.write(PACKAGE_INFO)

setuptools.setup(
    name="macrobond-data-api",
    packages=setuptools.find_packages(include=["macrobond_data_api", "macrobond_data_api.*"]),
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
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires=">=3.8",
    install_requires=[
        "keyring>=23.11.0",
        "Authlib>=1.2.0",
        "requests>=2.31.0",
        "ijson>=3.1.4",
        "pywin32>=305; os_name=='nt'",
    ],
    extras_require={
        "extra": ["matplotlib", "statsmodels", "scikit-learn", "pandas"],
        "dev": [
            "mypy==1.6.0",
            "pylint==3.0.1",
            "pycodestyle==2.11.1",
            "pdoc3==0.10.0",
            "build>=1.0.3",
            "pytest==7.4.2",
            "pytest-xdist==3.3.1",
            "coverage>=7.3.2",
            "black[jupyter]==23.9.1",
            "requests[socks]>=2.31.0",
            "nbconvert==7.3.0",
            "ipython>=7.34.0",
            "types-pywin32==306.0.0.5",
            "types-requests==2.31.0.9",
            "types-setuptools==68.2.0.0",
            "filelock==3.12.4",
        ],
        "socks": ["requests[socks]>=2.31.0"],
    },
    project_urls={
        "Documentation": "https://macrobond.github.io/macrobond-data-api",
        "Source": "https://github.com/macrobond/macrobond-data-api",
        "Tracker": "https://github.com/macrobond/macrobond-data-api/issues",
    },
)
