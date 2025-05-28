"""Setup configuration for the Fintual portfolio management package."""

from setuptools import find_packages, setup

setup(
    name="fintual-portfolio",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "matplotlib>=3.7.0",
    ],
    extras_require={
        "dev": [
            "black>=23.0.0",
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "ruff>=0.1.0",
        ],
    },
    python_requires=">=3.9",
    author="Felipe Silva",
    author_email="felipe.silva.v@gmail.com",
    description="A portfolio management system for Fintual",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/felipe-silva-v/fintual-portfolio",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
