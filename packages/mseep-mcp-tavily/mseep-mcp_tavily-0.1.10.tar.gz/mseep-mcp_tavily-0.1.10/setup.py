
from setuptools import setup, find_packages

setup(
    name="mseep-mcp_tavily",
    version="0.1.8",
    description="A Model Context Protocol server that provides AI-powered web search capabilities using Tavily's search API",
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
    install_requires=['mcp>=1.0.0', 'pydantic>=2.10.2', 'python-dotenv>=1.0.1', 'tavily-python>=0.5.0'],
    keywords=["mseep"] + [],
)
