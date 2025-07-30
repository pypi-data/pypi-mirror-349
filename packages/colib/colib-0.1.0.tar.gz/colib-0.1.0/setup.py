from setuptools import setup, find_packages

setup(
    name="colib",
    version="0.1.0",
    license="MIT",
    description="A simple color printing libary.",
    author="Amaan Syed",
    author_email="amaancal3@gmail.com",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", 
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)