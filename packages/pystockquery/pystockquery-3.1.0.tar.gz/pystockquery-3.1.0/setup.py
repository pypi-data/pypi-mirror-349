from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pystockquery",
    version="3.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A natural language interface for stock data analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pystockquery",
    packages=find_packages(),
    package_data={
        'pystockquery': ['data/*.xlsx'],
    },
    install_requires=[
        'pandas>=1.0.0',
        'openpyxl>=3.0.0',
        'matplotlib>=3.0.0',
        'seaborn>=0.11.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)