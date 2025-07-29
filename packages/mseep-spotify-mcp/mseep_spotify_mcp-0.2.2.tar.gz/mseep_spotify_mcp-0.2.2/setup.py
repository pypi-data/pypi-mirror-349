
from setuptools import setup, find_packages

setup(
    name="mseep-spotify-mcp",
    version="0.2.0",
    description="MCP spotify project",
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
    install_requires=['mcp==1.3.0', 'python-dotenv>=1.0.1', 'spotipy==2.24.0'],
    keywords=["mseep"] + [],
)
