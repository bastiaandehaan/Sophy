# setup.py
from setuptools import setup, find_packages

setup(
    name="sophy",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.20.0",
        "matplotlib>=3.4.0",
        "seaborn>=0.11.0",
        "MetaTrader5>=5.0.0",
    ],
    author="Sophy Trading Systems",
    author_email="info@sophytrading.com",
    description="Een Python-gebaseerd algoritmisch trading systeem met Turtle Trading strategie",
    keywords="trading, algoritm, metatrader, ftmo, turtle",
    url="https://github.com/yourusername/sophy",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.9",
)
