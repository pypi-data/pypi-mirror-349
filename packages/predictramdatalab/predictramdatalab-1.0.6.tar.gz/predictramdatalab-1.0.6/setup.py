from setuptools import setup, find_packages
from pathlib import Path

# Read long description from README.md
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="predictramdatalab",
    version="1.0.6",  # Increment this for each release
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "predictramdatalab": ["data/*.json"],
    },
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "matplotlib>=3.4.0",
        "openpyxl>=3.0.0",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python API for accessing and analyzing stock market data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/predictramdatalab",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    keywords="stocks finance market data analysis",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/predictramdatalab/issues",
        "Source": "https://github.com/yourusername/predictramdatalab",
    },
)