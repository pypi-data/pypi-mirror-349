"""Setup script for squad-builder package."""

import os
from setuptools import setup, find_packages

# Read the contents of the README file
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

# Set version number directly instead of importing from the package
version = '0.1.0'

setup(
    name="squad-builder",
    version=version,
    description="Unified cloud storage client for S3, Azure Blob, and GCP Storage",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Squad Builder Team",
    author_email="info@example.com",
    url="https://github.com/yourusername/squad-builder",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
        "boto3>=1.18.0",
        "azure-storage-blob>=12.8.0",
        "google-cloud-storage>=1.42.0",
        "fastapi>=0.100.0",
        "uvicorn>=0.22.0",
        "pyyaml>=6.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keywords="storage, s3, azure, gcp, cloud",
) 