import pathlib
from setuptools import setup

# The directory containing this file

# The text of the README file
README = (pathlib.Path(__file__).parent / "README.md").read_text()

setup(
    name="delegateto",
    author="Daniel Hilst Selli",
    author_email="danielhilst@gmail.com",
    version="1.5",
    py_modules=["delegateto"],
    python_requires=">=3",
    long_description=README,
    long_description_content_type="text/markdown",
    license="Apache-2.0",

)
