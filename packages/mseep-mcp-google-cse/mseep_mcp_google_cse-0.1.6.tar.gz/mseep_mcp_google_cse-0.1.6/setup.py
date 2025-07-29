
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-google-cse",
    version="0.1.4",
    description="An MCP server for searching a custom Google search engine.",
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
    install_requires=['mcp>=1.2.0', 'google-api-python-client>=2.159.0'],
    keywords=["mseep"] + ['MCP', 'Model Context Protocol', 'Google Custom Search Engine', 'Google CSE', 'Web Browsing'],
)
