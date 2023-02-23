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

REQUESTS_VERSION = "2.28.1"

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
        "Programming Language :: Python :: 3.7",
    ],
    python_requires=">=3.7",
    install_requires=[
        "keyring>=23.11.0",
        "Authlib>=1.2.0",
        "requests>=" + REQUESTS_VERSION,
        "python-dateutil>=2.8.2",
        "ijson>=3.1.4",
        "typing_extensions>=4.4.0",
        "pywin32>=305; os_name=='nt'",
    ],
    extras_require={
        "extra": ["matplotlib", "statsmodels", "scikit-learn", "pandas"],
        "dev": [
            "mypy==1.0.0",
            "pylint==2.15.8",
            "pycodestyle==2.10.0",
            "pdoc3==0.10.0",
            "build>=0.10.0",
            "pytest==7.2.1",
            "pytest-xdist==3.2.0",
            "coverage>=7.1.0",
            "black[jupyter]==23.1.0",
            "requests[socks]>=" + REQUESTS_VERSION,
            # types
            "types-pywin32==305.0.0.7",
            "types-python-dateutil==2.8.19.6",
            "types-requests==2.28.11.8",
            "types-setuptools==67.2.0.1",
        ],
        "socks": ["requests[socks]>=" + REQUESTS_VERSION],
    },
    project_urls={
        "Documentation": "https://macrobond.github.io/macrobond-data-api",
        "Source": "https://github.com/macrobond/macrobond-data-api",
        "Tracker": "https://github.com/macrobond/macrobond-data-api/issues",
    },
)
