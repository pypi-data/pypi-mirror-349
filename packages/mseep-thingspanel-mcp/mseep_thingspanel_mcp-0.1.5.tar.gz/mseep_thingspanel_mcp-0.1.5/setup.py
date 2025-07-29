
from setuptools import setup, find_packages

setup(
    name="mseep-thingspanel-mcp",
    version="0.1.4",
    description="MCP server for ThingsPanel IoT platform",
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
    install_requires=['mcp>=1.2.0', 'httpx>=0.23.0'],
    keywords=["mseep"] + [],
)
