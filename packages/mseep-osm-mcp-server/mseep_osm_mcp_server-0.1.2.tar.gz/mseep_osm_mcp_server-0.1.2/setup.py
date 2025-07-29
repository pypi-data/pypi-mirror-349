
from setuptools import setup, find_packages

setup(
    name="mseep-osm-mcp-server",
    version="0.1.1",
    description="An OpenStreetMap MCP server",
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
    install_requires=['aiohttp>=3.11.13', 'mcp[cli]>=1.3.0'],
    keywords=["mseep"] + [],
)
