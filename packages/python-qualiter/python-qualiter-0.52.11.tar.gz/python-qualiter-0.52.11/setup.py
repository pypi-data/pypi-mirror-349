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
    version="0.52.11",
    url="https://gitlab.com/rbacovic/python-qualiter",
    description="A modern Click-based CLI tool for running multiple linting tools on Python files with a clean visual output.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Radovan Bacovic",
    author_email="radovan.bacovic@gmail.com",
    packages=find_packages(),
    package_dir={"": "."},
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[
        "click>=8.0.0",
        "isort>=5.10.0",
        "black>=22.0.0",
        "mypy>=0.950",
        "flake8>=4.0.0",
        "pylint>=2.12.0",
        "vulture>=2.3",
        "tomli>=1.1.0; python_version >= '3.6'",
        "typing-extensions>=4.0.0",
        "pathspec>=0.9.0",
        "platformdirs>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "python-qualiter=src.app:cli",
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
