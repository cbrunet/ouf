from setuptools import setup, find_packages

setup(
    name="Ouf",
    version="0.0.0.0-dev",

    packages=find_packages('src'),
    package_dir={'': 'src'},
    entry_points={
        'gui_scripts': [
            'ouf = ouf.main:main'
        ]
    },


    author="Charles Brunet",
    author_email="charles@cbrunet.net",
    description="Organiseur Universel de Fichiers (Universal File Organizer)",
    license='GPLv3',
    keywords="",
    url="https://github.com/cbrunet/ouf"
)