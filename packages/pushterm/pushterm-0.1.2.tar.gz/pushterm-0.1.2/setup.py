# setup.py

from setuptools import setup, find_packages

setup(
    name="pushterm",
    version="0.1.2",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    entry_points=
    {
        'console_scripts': 
        [
            'pushterm=pushterm.__main__:main',
        ],
    },

)
