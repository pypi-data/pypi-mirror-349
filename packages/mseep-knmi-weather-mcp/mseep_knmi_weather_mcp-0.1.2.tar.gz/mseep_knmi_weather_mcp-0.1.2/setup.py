
from setuptools import setup, find_packages

setup(
    name="mseep-knmi-weather-mcp",
    version="0.1.0",
    description="KNMI Weather MCP Server",
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
    install_requires=['fastmcp', 'httpx', 'pydantic', 'python-dotenv', 'pytest', 'polars', 'xarray', 'numpy', 'netCDF4', 'pydantic-settings>=2.7.1'],
    keywords=["mseep"] + [],
)
