"""
Setup configuration for RHD Bearings Product Catalog Generator.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read version from __init__.py
version_file = this_directory / "rhd_bearings" / "__init__.py"
version_line = [line for line in version_file.read_text().splitlines() if line.startswith("__version__")][0]
version = version_line.split('"')[1]

setup(
    name="rhd-bearings-catalog",
    version=version,
    author="RHD Bearings",
    author_email="sales@rhdenterprise.in",
    description="Professional bearing catalog generator with SEO and LLM optimization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://rhdbearings.com",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Manufacturing",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        # No external dependencies - uses only Python standard library
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.9",
            "mypy>=0.910",
        ],
    },
    entry_points={
        "console_scripts": [
            "rhd-bearings=rhd_bearings.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "rhd_bearings": [
            "data/*.json",
            "data/*.md",
        ],
    },
    zip_safe=False,
    keywords="bearings catalog generator seo manufacturing industrial",
    project_urls={
        "Bug Reports": "https://rhdbearings.com/contact",
        "Company": "https://rhdbearings.com",
        "Source": "https://rhdbearings.com",
    },
)
