from setuptools import setup, find_packages

setup(
    name="geneticops",
    version="0.1.0",
    author="Juan David Moreno Beltran",
    author_email="jdmoreno@gmail.com",
    description="Librería de algoritmos genéticos en Python",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "numpy>=1.18.0",
        "matplotlib>=3.3.0",
    ],
    
)

