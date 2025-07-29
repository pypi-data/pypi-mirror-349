
from setuptools import setup, find_packages

setup(
    name="mseep-onos-mcp-server",
    version="0.1.0",
    description="MCP server for ONOS network management",
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
    install_requires=['httpx>=0.28.1', 'mcp>=1.5.0'],
    keywords=["mseep"] + [],
)
