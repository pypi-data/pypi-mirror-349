
from setuptools import setup, find_packages

setup(
    name="mseep-python-server-mcp",
    version="0.1.0",
    description="MCP server for cryptocurrency price information",
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
    install_requires=['httpx>=0.28.1', 'mcp[cli]>=1.6.0', 'pydantic>=2.11.1', 'pydantic-settings>=2.8.1', 'python-coinmarketcap>=0.6', 'python-decouple>=3.8'],
    keywords=["mseep"] + [],
)
