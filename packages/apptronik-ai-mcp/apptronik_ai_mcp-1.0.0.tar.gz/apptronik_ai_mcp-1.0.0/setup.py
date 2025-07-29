from setuptools import setup, find_packages

setup(
    name="apptronik-ai-mcp",
    version="1.0.0",
    description="Model Context Protocol (MCP) integration for Apptronik AI - Automated Crypto Asset Management",
    author="Apptronik AI Team",
    author_email="help@apptronik-ai.com",
    url="https://www.apptronik-ai.com",
    packages=find_packages(),
    install_requires=[
        "web3>=6.11.1",
        "solana>=0.30.2",
        "python-binance>=1.0.19",
        "tensorflow>=2.15.0",
        "numpy>=1.24.0",
        "pandas>=2.1.0",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
) 