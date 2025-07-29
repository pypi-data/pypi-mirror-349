"""
Setup script for PreProPy package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="prepropy",
    version="0.1.0",
    author="PreProPy Team",
    author_email="example@example.com",
    description="A Python package combining essential preprocessing tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/prepropy",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.7",    install_requires=[
        "pandas>=1.0.0",
        "scikit-learn>=0.24.0",
    ],
    extras_require={
        'dev': [
            'pytest>=6.0.0',
            'pytest-cov>=2.12.0',
            'black>=21.5b2',
            'isort>=5.9.1',
            'flake8>=3.9.2',
        ],    },
    entry_points={
        'console_scripts': [
            'prepropy=prepropy.cli:main',
        ],
    },
    keywords="preprocessing, data science, machine learning, pandas, scikit-learn",
)
