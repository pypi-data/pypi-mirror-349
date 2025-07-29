
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-server-redis",
    version="0.1.0",
    description="MCP server to interact with redis server, aws memory DB, etc for caching or other use-cases where in-memory and key-value based storage is appropriate",
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
    install_requires=['mcp[cli]>=1.2.1', 'python-dotenv>=1.0.1', 'redis>=5.2.1'],
    keywords=["mseep"] + [],
)
