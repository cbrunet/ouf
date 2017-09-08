from setuptools import setup, find_packages

setup(
    name="Ouf",
    version="0.0.0.0-dev",
    packages=find_packages(exclude=["test"]),
    entry_points={
        'gui_scripts': [
            'ouf = ouf.main:main'
        ]
    }
)