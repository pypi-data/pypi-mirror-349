# setup.py
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="portwarden",
    version="1.0.1",
    author="B14CK-KN1GH7",
    description="A fast multi-threaded TCP port scanner with JSON output.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nfs-tech-bd/portwarden ",
    packages=find_packages(),
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Security",
        "Environment :: Console",
    ],
    python_requires='>=3.6',
    entry_points={
        "console_scripts": [
            "portwarden=portwarden.portwarden:main",
        ],
    },
)