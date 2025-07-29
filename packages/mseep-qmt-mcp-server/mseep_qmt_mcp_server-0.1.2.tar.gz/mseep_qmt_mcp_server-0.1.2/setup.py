
from setuptools import setup, find_packages

setup(
    name="mseep-qmt-mcp-server",
    version="0.1.0",
    description="MCP Server for QMT",
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
    install_requires=['mcp>=1.6.0', 'pyyaml>=6.0.2', 'xtquant>=241014.1.2'],
    keywords=["mseep"] + [],
)
