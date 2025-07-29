from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="predictram_PyRatio",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A package for analyzing stock financial metrics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/predictram_PyRatio",
    packages=find_packages(),
    package_data={
        'predictram_PyRatio': ['data/*.json'],
    },
    install_requires=[
        'pandas>=1.0',
        'numpy>=1.0',
        'matplotlib>=3.0',
        'seaborn>=0.11',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)