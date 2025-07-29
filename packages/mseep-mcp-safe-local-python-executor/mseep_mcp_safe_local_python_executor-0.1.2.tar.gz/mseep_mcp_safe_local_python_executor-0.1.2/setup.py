
from setuptools import setup, find_packages

setup(
    name="mseep-mcp_safe_local_python_executor",
    version="0.1.0",
    description="MCP server exposing tool for a safe local Python code execution",
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
    install_requires=['mcp[cli]>=1.5.0', 'smolagents==1.12.0'],
    keywords=["mseep"] + [],
)
