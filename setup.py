from setuptools import find_packages, setup

setup(
    name="turing-machine-py",
    version="0.1.0",
    packages=find_packages(where="src"),
    python_requires=">=3.9, <4",
)
