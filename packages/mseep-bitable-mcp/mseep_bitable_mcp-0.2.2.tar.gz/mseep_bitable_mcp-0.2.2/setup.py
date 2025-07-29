
from setuptools import setup, find_packages

setup(
    name="mseep-bitable-mcp",
    version="0.2.1",
    description="This MCP server provides access to Lark bitable through the Model Context Protocol.",
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
    install_requires=['pybitable', 'mcp==1.3.0', 'typer'],
    keywords=["mseep"] + [],
)
