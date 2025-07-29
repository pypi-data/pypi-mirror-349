
from setuptools import setup, find_packages

setup(
    name="mseep-cryo-mcp",
    version="0.1.4",
    description="MCP server for querying Ethereum blockchain data using cryo",
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
    install_requires=['duckdb>=1.2.1', 'mcp>=1.3.0', 'numpy>=2.2.3', 'pandas>=2.2.3', 'pyarrow>=19.0.1', 'requests>=2.28.0'],
    keywords=["mseep"] + ['ethereum', 'blockchain', 'cryo', 'mcp', 'api', 'server'],
)
