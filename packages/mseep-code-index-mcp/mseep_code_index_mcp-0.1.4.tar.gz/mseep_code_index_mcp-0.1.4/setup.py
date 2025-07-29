
from setuptools import setup, find_packages

setup(
    name="mseep-code-index-mcp",
    version="0.1.2",
    description="Code indexing and analysis tools for LLMs using MCP",
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
    install_requires=['mcp>=0.3.0'],
    keywords=["mseep"] + [],
)
