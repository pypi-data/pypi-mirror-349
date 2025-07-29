from setuptools import setup, find_packages

setup(
    name="ta_dict",
    version="0.0.1",
    packages=find_packages(),
    description="A fast, dependency-free technical analysis library using Python nested dictionaries.",
    long_description=open("README.md").read() +'\n\n' + open('CHANGELOG.txt').read(),
    long_description_content_type="text/markdown",
    author="Faryad97",
    author_email="admin@rasalgeti.com",
    url="https://github.com/faryad97/ta_dict",  # Update if available
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.0",
    install_requires=[],  # No dependencies!
)
