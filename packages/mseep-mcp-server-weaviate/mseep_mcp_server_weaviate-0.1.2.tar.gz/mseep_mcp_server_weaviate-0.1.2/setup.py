
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-server-weaviate",
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
    install_requires=['weaviate-client==4.10.4'],
    keywords=["mseep"] + [],
)
