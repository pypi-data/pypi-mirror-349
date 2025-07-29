from setuptools import setup, find_packages

setup(
    name="predictramdatalab",
    version="1.0.4",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "predictramdatalab": ["data/*.json"],
    },
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "openpyxl",  # For Excel export
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python API for accessing and analyzing stock data",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/predictramdatalab",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)