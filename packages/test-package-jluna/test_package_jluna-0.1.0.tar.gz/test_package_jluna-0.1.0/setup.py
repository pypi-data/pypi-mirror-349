from setuptools import setup, find_packages

setup(
    name="test-package-jluna",  # Usa un nombre único
    version="0.1.0",
    description="A test Python package for upload testing",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Johan Luna",
    author_email="johan.luna@finkargo.com",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)