
from setuptools import setup, find_packages

setup(
    name="mseep-flights-mcp",
    version="0.1.0",
    description="Flight search MCP server using Duffel API",
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
    install_requires=['httpx', 'python-dotenv', 'pydantic', 'mcp'],
    keywords=["mseep"] + [],
)
