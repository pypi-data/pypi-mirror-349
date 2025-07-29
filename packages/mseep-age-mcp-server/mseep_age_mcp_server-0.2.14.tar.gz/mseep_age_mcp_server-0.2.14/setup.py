
from setuptools import setup, find_packages

setup(
    name="mseep-age-mcp-server",
    version="0.2.12",
    description="Apache AGE MCP Server",
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
    install_requires=['agefreighter>=1.0.7', 'mcp>=1.9.0', 'ply>=3.11', 'psycopg[binary,pool]>=3.2.9'],
    keywords=["mseep"] + [],
)
