#Setup.py

from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name= 'librerias_ag',
    version='0.1.1',
    author="Jorge Salazar",
    author_email="jisalazar@ucundinamarca.edu.co",
    description="Una libreria para Algoritmos Geneticos",
    long_description=long_description,  # Long description from README.md
    long_description_content_type="text/markdown",
    url="https://github.com/JSalazar17/librerias_ag",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[

    "numpy"

    ],
)