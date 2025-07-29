
from setuptools import setup, find_packages

setup(
    name="mseep-rootly-mcp-server",
    version="1.0.0",
    description="A Model Context Protocol server for Rootly APIs using OpenAPI spec",
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
    install_requires=['mcp>=1.1.2', 'requests>=2.28.0', 'pydantic>=2.0.0'],
    keywords=["mseep"] + ['rootly', 'mcp', 'llm', 'automation', 'incidents'],
)
