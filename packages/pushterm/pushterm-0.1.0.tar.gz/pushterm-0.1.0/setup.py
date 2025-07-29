from setuptools import setup, find_packages

setup(
    name="pushterm",
    version="0.1.0",
    author="Andrew Ehli",
    author_email="you@example.com",
    description="A simple terminal UI tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Andrews3dfactory/pushterm",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
