
from setuptools import setup, find_packages

setup(
    name="mseep-markitdown-mcp-server",
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
    install_requires=['markitdown>=0.1', 'mcp>=1.2.1'],
    keywords=["mseep"] + [],
)
