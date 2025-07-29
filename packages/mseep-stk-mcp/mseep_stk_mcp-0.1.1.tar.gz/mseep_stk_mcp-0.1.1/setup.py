
from setuptools import setup, find_packages

setup(
    name="mseep-stk-mcp",
    version="0.1.0",
    description="STK-MCP, an MCP server allowing LLMs to interact with Ansys/AGI STK - Digital Mission Engineering Software",
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
    install_requires=['mcp[cli]>=1.6.0'],
    keywords=["mseep"] + [],
)
