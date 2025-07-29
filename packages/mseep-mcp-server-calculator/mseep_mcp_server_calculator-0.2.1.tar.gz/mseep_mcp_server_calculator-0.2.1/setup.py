
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-server-calculator",
    version="0.2.0",
    description="A Model Context Protocol server for calculating",
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
    install_requires=['mcp>=1.4.1'],
    keywords=["mseep"] + ['mcp', 'llm', 'math', 'calculator'],
)
