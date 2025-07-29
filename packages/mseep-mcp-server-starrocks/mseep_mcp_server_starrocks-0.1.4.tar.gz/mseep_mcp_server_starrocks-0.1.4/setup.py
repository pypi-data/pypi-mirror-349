
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-server-starrocks",
    version="0.1.2",
    description="official MCP server for StarRocks",
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
    install_requires=['kaleido==0.2.1', 'mcp>=1.0.0', 'mysql-connector-python>=9.2.0', 'pandas>=2.2.3', 'plotly>=6.0.1'],
    keywords=["mseep"] + [],
)
