
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-server-ietf",
    version="0.1.0",
    description="A Model Context Protocol server for fetching ietf documents for LLMs",
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
    install_requires=['mcp[cli]>=1.3.0', 'python-dotenv>=1.0.1', 'requests>=2.32.3'],
    keywords=["mseep"] + [],
)
