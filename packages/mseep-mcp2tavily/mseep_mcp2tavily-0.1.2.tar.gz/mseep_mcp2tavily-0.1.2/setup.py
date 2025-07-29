
from setuptools import setup, find_packages

setup(
    name="mseep-mcp2tavily",
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
    install_requires=['fastmcp>=0.4.1', 'load-dotenv>=0.1.0', 'tavily-python>=0.5.0', 'uvicorn>=0.34.0'],
    keywords=["mseep"] + [],
)
