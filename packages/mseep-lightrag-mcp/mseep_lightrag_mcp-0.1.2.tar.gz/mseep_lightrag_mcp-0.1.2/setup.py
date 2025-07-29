
from setuptools import setup, find_packages

setup(
    name="mseep-lightrag_mcp",
    version="0.1.0",
    description="MCP Server for LightRAG",
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
    install_requires=['mcp>=1.2.0', 'httpx>=0.28.1', 'pydantic>=2.11', 'python-dotenv>=1.0.1', 'attrs>=25.3.0'],
    keywords=["mseep"] + [],
)
