
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-email-client",
    version="0.1.0",
    description="Add your description here",
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
    install_requires=['asyncio>=3.4.3', 'duckdb>=1.2.2', 'imapclient>=3.0.1', 'mcp[cli]>=1.3.0', 'numpy>=2.2.4', 'pydantic>=2.10.6', 'sentence-transformers>=4.1.0'],
    keywords=["mseep"] + [],
)
