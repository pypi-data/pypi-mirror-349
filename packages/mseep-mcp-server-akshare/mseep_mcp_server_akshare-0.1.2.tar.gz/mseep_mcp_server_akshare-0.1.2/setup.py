
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-server-akshare",
    version="0.1.0",
    description="MCP server for AKShare financial data",
    author="mseep",
    author_email="support@skydeck.ai",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=['akshare>=1.11.0', 'mcp>=0.1.0', 'httpx>=0.24.0', 'python-dotenv>=1.0.0', 'pandas>=2.0.0', 'numpy>=1.24.0'],
    keywords=["mseep"] + [],
)
