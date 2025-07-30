import setuptools
from pathlib import Path

setuptools.setup(
    name="youngpdf",
    version=1.0,
    long_description=Path("READEME.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests", "data"])
)
