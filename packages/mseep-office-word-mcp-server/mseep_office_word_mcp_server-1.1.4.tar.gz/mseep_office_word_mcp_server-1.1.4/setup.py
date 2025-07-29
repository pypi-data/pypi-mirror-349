
from setuptools import setup, find_packages

setup(
    name="mseep-office-word-mcp-server",
    version="1.1.3",
    description="MCP server for manipulating Microsoft Word documents",
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
    install_requires=['python-docx>=0.8.11', 'mcp[cli]>=1.3.0', 'msoffcrypto-tool>=5.4.2', 'docx2pdf>=0.1.8'],
    keywords=["mseep"] + [],
)
