from setuptools import setup, find_packages


with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="ml-gen-alg",
    version="1.0.5",
    author="Nicolas Torres & Yamid Quiroga",
    author_email="yfquiroga@ucundinamarca.edu.co",
    description="Una librería de algoritmos genéticos en Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YFQG/ml-gen-alg",  # Reemplaza con tu URL real
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "setuptools",
        "wheel",
        "twine"],  # Agrega dependencias si es necesario
)

