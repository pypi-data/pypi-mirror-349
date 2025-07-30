from setuptools import setup, find_packages

setup(
    name="csv-analyzer1",
    version="0.1.1",
    packages=find_packages(),
    install_requires=["pydantic"],
    author="Theme 7",
    description="Analyseur de CSV avec validation de données"
)