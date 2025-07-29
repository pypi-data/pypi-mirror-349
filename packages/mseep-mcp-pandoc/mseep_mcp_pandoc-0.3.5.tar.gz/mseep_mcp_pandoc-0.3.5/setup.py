
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-pandoc",
    version="0.3.3",
    description="MCP to interface with pandoc to convert files to differnt formats. Eg: Converting markdown to pdf.",
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
    install_requires=['mcp>=1.1.0', 'pandoc>=2.4', 'pypandoc>=1.14'],
    keywords=["mseep"] + [],
)
