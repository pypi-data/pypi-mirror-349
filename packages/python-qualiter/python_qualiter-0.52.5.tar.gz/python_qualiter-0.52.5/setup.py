"""
Setup file for the python-qualiter project
```
"""

from pathlib import Path

from setuptools import find_packages, setup


this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="python-qualiter",
    version="0.52.5",
    url="https://gitlab.com/rbacovic/python-qualiter",
    description="A modern Click-based CLI tool for running multiple linting tools on Python files with a clean visual output.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Radovan Bacovic",
    author_email="radovan.bacovic@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "python-qualiter=app:cli",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
