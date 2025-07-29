
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-trader",
    version="0.1.0",
    description="A sample MCP server for traders",
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
    install_requires=['aiohttp>=3.11.11', 'mcp>=1.2.0', 'numpy==1.26.4', 'pandas>=2.2.3', 'pandas-ta>=0.3.14b0', 'python-dotenv>=1.0.1', 'setuptools>=75.8.0', 'ta-lib>=0.6.0'],
    keywords=["mseep"] + [],
)
