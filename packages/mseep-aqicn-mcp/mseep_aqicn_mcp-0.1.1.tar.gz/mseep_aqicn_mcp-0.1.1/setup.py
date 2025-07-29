
from setuptools import setup, find_packages

setup(
    name="mseep-aqicn-mcp",
    version="0.1.0",
    description="MCP server for fetching air quality data from AQICN",
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
    install_requires=['mcp[cli]', 'httpx', 'pydantic>=2.0.0', 'python-dotenv>=1.0.0'],
    keywords=["mseep"] + [],
)
