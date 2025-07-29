
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-server-everything-search",
    version="0.2.1",
    description="A Model Context Protocol server providing fast file searching using Everything SDK",
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
    install_requires=['mcp>=1.0.0', 'pydantic>=2.0.0'],
    keywords=["mseep"] + ['everything', 'search', 'mcp', 'llm'],
)
