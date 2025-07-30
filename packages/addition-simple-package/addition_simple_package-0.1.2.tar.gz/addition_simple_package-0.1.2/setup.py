from setuptools import setup, find_packages

setup(
    name="addition-simple-package",
    version="0.1.2",
    description="A simple Python package that adds up",
    author="Yerly Sevan",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
