"""
Setup script for the MCP Solana package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mcp-solana",
    version="0.1.0",
    author="LYRAIOS Team",
    author_email="info@lyraios.ai",
    description="Model Context Protocol (MCP) integration for Solana blockchain",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GalaxyLLMCI/lyraios.git",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache License 2.0",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "aiohttp>=3.8.0",
        "pydantic>=1.9.0",
        "solana>=0.29.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.18.0",
            "black>=22.0.0",
            "isort>=5.10.0",
            "mypy>=0.931",
            "sphinx>=4.4.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
    },
) 