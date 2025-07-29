
from setuptools import setup, find_packages

setup(
    name="mseep-memory-journal-mcp-server",
    version="0.1.0",
    description="MCP server for memory journal from local photos (iCloud Photos)",
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
    install_requires=['dateparser>=1.2.0', 'httpx>=0.28.1', 'mcp>=1.2.0', 'osxphotos>=0.69.2', 'spacy>=3.8.4', 'thefuzz>=0.22.1'],
    keywords=["mseep"] + [],
)
