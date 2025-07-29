
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-nefino",
    version="0.1.5",
    description="MCP server for accessing Nefino renewable energy news API",
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
    install_requires=['mcp>=1.3.0', 'requests', 'python-jose', 'pydantic', 'fastapi', 'aiohttp'],
    keywords=["mseep"] + [],
)
