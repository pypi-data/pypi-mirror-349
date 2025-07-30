"""
Setup script for the EOL Timeline package.
"""
from setuptools import setup, find_packages
from eol_timeline import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="eol-timeline",
    version=__version__,
    author="EOL Timeline Contributors",
    author_email="",
    description="A tool for tracking software end-of-life dates",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
    install_requires=[
        "typer>=0.9.0",
        "rich>=13.5.0",
        "pyyaml>=6.0",
        "python-dateutil>=2.8.2",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "mypy>=1.0.0",
            "flake8>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "eol=eol_timeline.cli:main",
        ],
    },
)
