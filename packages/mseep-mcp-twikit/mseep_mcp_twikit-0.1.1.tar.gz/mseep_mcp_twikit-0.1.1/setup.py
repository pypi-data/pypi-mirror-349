
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-twikit",
    version="0.1.0",
    description="Twitter search tool for FastMCP using Twikit",
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
    install_requires=['fastmcp', 'twikit', 'requests'],
    keywords=["mseep"] + [],
)
