
from setuptools import setup, find_packages

setup(
    name="mseep-eka_mcp_server",
    version="0.2.4",
    description="The official Eka MCP Server for medical science tools curated by eka.care",
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
    install_requires=['mcp>=1.3.0', 'httpx>=0.28.1', 'logging>=0.4.9.6', 'pillow>=11.0.0', 'pytest>=8.3.5', 'pyjwt>=2.10.0'],
    keywords=["mseep"] + [],
)
