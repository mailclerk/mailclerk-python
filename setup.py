import pathlib
from setuptools import setup

from mailclerk import __version__

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="mailclerk",
    version=str(__version__),
    description="Send mail with mailclerk.app",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/mailclerk/mailclerk-python",
    author="Greg Sherrid",
    author_email="developers@mailclerk.app",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
    ],
    packages=["mailclerk"],
    include_package_data=False,
    install_requires=[
        'requests >= 2.20; python_version >= "3.0"',
        'requests[security] >= 2.20; python_version < "3.0"',
    ],
)
