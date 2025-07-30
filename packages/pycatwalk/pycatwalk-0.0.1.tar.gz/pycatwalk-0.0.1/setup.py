import os
from setuptools import setup, find_packages

# Read the contents of the README file
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

# Define package metadata
setup(
    name="pycatwalk",
    version="0.0.1",  # Using the version from Constants in core/enums.py
    author="Catwalk Team",
    author_email="wawanb.setyawan@gmail.com",  # Replace with your actual email
    description="An elegant framework for cross-platform AI model execution with intelligent caching",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wansatya/pycatwalk",  # Replace with your actual repository URL
    packages=find_packages(exclude=["tests", "examples"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy>=1.19.0",
        "psutil>=5.8.0",
    ],
    extras_require={
        "torch": ["torch>=1.9.0"],
        "onnx": ["onnxruntime>=1.8.0", "onnx>=1.10.0"],
        "huggingface": ["transformers>=4.5.0"],
        "tensorflow": ["tensorflow>=2.5.0"],
        "all": [
            "torch>=1.9.0",
            "onnxruntime>=1.8.0",
            "onnx>=1.10.0",
            "transformers>=4.5.0",
            "tensorflow>=2.5.0",
        ],
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.12.0",
            "black>=21.5b2",
            "isort>=5.9.1",
            "flake8>=3.9.2",
            "mypy>=0.812",
        ],
    },
    keywords="machine learning, model deployment, performance optimization, caching, cross-platform",
    project_urls={
        "Bug Reports": "https://github.com/wansatya/pycatwalk/issues",
        "Source": "https://github.com/wansatya/pycatwalk",
        "Documentation": "https://pycatwalk.readthedocs.io/",
    },
)
