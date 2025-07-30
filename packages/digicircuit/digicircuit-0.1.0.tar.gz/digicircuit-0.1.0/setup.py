from setuptools import setup, find_packages

setup(
    name="digicircuit",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "openpyxl",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A package for converting Boolean expressions to circuit diagrams",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/digicircuit",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "digicircuit=digicircuit.boolean_to_circuit:main",
        ],
    },
)