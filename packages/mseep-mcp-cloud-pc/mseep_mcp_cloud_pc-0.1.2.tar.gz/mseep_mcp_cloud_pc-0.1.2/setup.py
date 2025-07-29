
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-cloud-pc",
    version="0.1.0",
    description="Windows 365 Cloud PC Management MCP Server",
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
    install_requires=['mcp>=1.5.0'],
    keywords=["mseep"] + [],
)
