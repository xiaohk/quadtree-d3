#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.md") as readme_file:
    readme = readme_file.read()

requirements = ["tqdm", "numpy"]

test_requirements = [
    "pytest>=3",
]

setup(
    author="Quadtree",
    author_email="jay@zijie.wang",
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    description="Quadtree implementation in Python following the d3-quadtree's structure",
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="quadtreed3",
    name="quadtreed3",
    packages=find_packages(include=["quadtreed3", "quadtreed3.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/xiaohk/quadtreed3",
    version="0.1.1",
    zip_safe=False,
)
