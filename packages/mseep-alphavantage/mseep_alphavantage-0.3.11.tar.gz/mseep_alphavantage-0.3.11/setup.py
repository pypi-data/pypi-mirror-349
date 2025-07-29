
from setuptools import setup, find_packages

setup(
    name="mseep-alphavantage",
    version="0.3.10",
    description="Alphavantage MCP server",
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
    install_requires=['bump2version>=1.0.1', 'load-dotenv>=0.1.0', 'mcp>=1.0.0', 'toml>=0.10.2'],
    keywords=["mseep"] + [],
)
