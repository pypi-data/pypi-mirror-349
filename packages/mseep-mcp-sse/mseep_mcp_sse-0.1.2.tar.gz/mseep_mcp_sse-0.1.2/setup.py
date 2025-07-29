
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-sse",
    version="0.1.0",
    description="SSE-based MCP Server and Client",
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
    install_requires=['argparse>=1.4.0', 'httpx>=0.28.1', 'mcp[cli]>=1.2.1', 'python-dotenv>=1.0.1', 'paramiko>=3.5.1', 'pymetasploit3>=1.0.6'],
    keywords=["mseep"] + [],
)
