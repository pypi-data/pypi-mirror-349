
from setuptools import setup, find_packages

setup(
    name="mseep-unichat-mcp-server",
    version="0.2.19",
    description="Unichat MCP Server",
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
    install_requires=['mcp>=1.0.0', 'unichat~=3.6.0'],
    keywords=["mseep"] + [],
)
